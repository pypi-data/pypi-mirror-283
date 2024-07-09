from . import making_script
from . import mapping
from . import reducing
from . import polling
from . import utils
from . import debugging
from .. import calling
from ... import utils as general_utils
from .. import organizing_jobs

import json_line_logger
import rename_after_writing
import os
import time
import shutil
import copy
import json


class Pool:
    """
    A pool of compute resources on a distributed compute cluster
    using slurm's sbatch --array.
    """

    def __init__(
        self,
        num_simultaneously_running_tasks=None,
        python_path=None,
        polling_interval=5.0,
        work_dir=None,
        keep_work_dir=False,
        verbose=False,
        slurm_call_timeout=60.0,
        max_num_resubmissions=None,
        sbatch_path="sbatch",
        squeue_path="squeue",
        scancel_path="scancel",
    ):
        """
        Parameters
        ----------
        num_simultaneously_running_tasks : int or None
            Up to this many tasks will run in parallel.
        python_path : str or None
            The python path to be used on the computing-cluster's worker-nodes
            to execute the worker-node's python-script.
        polling_interval : float or None
            The time in seconds to wait before polling squeue again while
            waiting for the jobs to finish.
        work_dir : str
            The directory path where the tasks, the results and the
            worker-node-script is stored.
        keep_work_dir : bool
            When True, the working directory will not be removed.
        verbose : bool
            If true, the pool will print the state of its jobs to stdout.
        slurm_call_timeout : float
            Timeout for calling sbatch, squeue, and scancel in seconds.
        max_num_resubmissions : None
            In case of error like states, the job will be tried this
            often to be resubmitted befor giving up on it.

        Returns
        -------
        pool : pypoolparty.slurm.array.Pool
            A pool instance with a map() function.
        """

        if python_path is None:
            self.python_path = general_utils.default_python_path()
        else:
            self.python_path = python_path

        self.work_dir = work_dir
        self.polling_interval = float(polling_interval)
        assert self.polling_interval > 0.0
        self.keep_work_dir = bool(keep_work_dir)
        self.num_simultaneously_running_tasks = (
            num_simultaneously_running_tasks
        )
        self.slurm_call_timeout = float(slurm_call_timeout)
        assert self.slurm_call_timeout >= 0.0

        self.max_num_resubmissions = max_num_resubmissions
        self.verbose = bool(verbose)

        self.sbatch_path = sbatch_path
        self.squeue_path = squeue_path
        self.scancel_path = scancel_path

    def __repr__(self):
        return self.__class__.__name__ + "()"

    def print(self, msg):
        print("[pypoolparty]", general_utils.time_now_iso8601(), msg)

    def map(
        self, func, iterable, chunksize=None, _unpack_task_with_asterisk=False
    ):
        """
        Apply `func` to each element in `iterable`, collecting the results
        in a list that is returned.

        Parameters
        ----------
        func : function-pointer
            Pointer to a function in a python-module. It must have both:
            func.__module__
            func.__name__
        iterable : list
            List of tasks. Each task must be a valid input to 'func'.
        chunksize : int
            This is ignored for the SLURM array.

        Returns
        -------
        results : list
            Results. One result for each task.

        Example
        -------
        results = pool.map(sum, [[1, 2], [2, 3], [4, 5], ])
            [3, 5, 9]
        """
        opj = os.path.join

        tasks = iterable  # to be consistent with multiprocessing's pool.map.

        if len(tasks) == 0:
            return []

        ## START UP
        ## ========

        # work_dir
        # --------
        jobname = general_utils.session_id_from_time_now()
        if self.work_dir is None:
            work_dir = os.path.abspath(
                opj(".", ".pypoolparty_slurm_array_" + jobname)
            )
        else:
            work_dir = os.path.join(os.path.abspath(self.work_dir), jobname)
        os.makedirs(work_dir)

        # logger
        # ------
        logger = json_line_logger.LoggerFile(path=opj(work_dir, "log.jsonl"))

        # start
        # -----
        _start_msg = "start: {:s}".format(work_dir)
        logger.debug(_start_msg)
        if self.verbose:
            self.print(_start_msg)

        # making the script to be executed by the worker-nodes
        # ----------------------------------------------------
        logger.debug("Making script...")
        script_content = making_script.make(
            func_module=func.__module__,
            func_name=func.__name__,
            shebang="#!{:s}".format(self.python_path),
            work_dir=work_dir,
            unpack_task_with_asterisk=_unpack_task_with_asterisk,
        )
        general_utils.write_text(
            path=opj(work_dir, "script.py"), content=script_content
        )
        general_utils.make_path_executable(path=opj(work_dir, "script.py"))
        logger.debug("Making script: done.")

        # writing the tasks into the work_dir
        # -----------------------------------
        logger.debug("Mapping {:d} tasks...".format(len(tasks)))
        mapping.write_tasks_to_work_dir(work_dir=work_dir, tasks=tasks)
        logger.debug("Mapping {:d} tasks: done.".format(len(tasks)))

        # initial call of sbatch --array
        # ------------------------------
        logger.debug("Calling sbatch --array...")
        calling.sbatch(
            script_path=opj(work_dir, "script.py"),
            stdout_path=opj(work_dir, "%a.stdout"),
            stderr_path=opj(work_dir, "%a.stderr"),
            jobname=jobname,
            array=True,
            array_start_task_id=0,
            array_stop_task_id=len(iterable) - 1,
            array_num_simultaneously_running_tasks=self.num_simultaneously_running_tasks,
            logger=logger,
            sbatch_path=self.sbatch_path,
            timeout=self.slurm_call_timeout,
        )
        logger.debug("Calling sbatch --array: done.")

        ## WAITING FOR TASKS TO RETURN A.K.A. BABYSITTING SLURM
        ## ====================================================
        logger.debug("Preparing reduction of results...")
        with reducing.Reducer(work_dir=work_dir) as reducer:
            logger.debug("Preparing reduction of results: done.")

            logger.debug("Waiting for tasks to return...")

            num_resubmissions_by_array_task_id = {}
            last_poll = polling.init(len_tasks=len(tasks))

            while True:
                # Collecting/reducing task results written by the worker nodes
                # ------------------------------------------------------------
                reducer.reduce()

                # Babysitting SLURM
                # -----------------
                (
                    num_resubmissions_by_array_task_id,
                    jobs,
                ) = self.resubmit_jobs_which_indicate_errors_and_might_profit_from_a_resubmission(
                    num_resubmissions_by_array_task_id=num_resubmissions_by_array_task_id,
                    work_dir=work_dir,
                    jobname=jobname,
                    logger=logger,
                )

                # printing/logging current polling state
                # --------------------------------------
                poll = polling.init(
                    len_tasks=len(tasks),
                    reducer=reducer,
                    jobs=jobs,
                    num_resubmissions_by_array_task_id=num_resubmissions_by_array_task_id,
                )
                poll_msg = polling.to_str(poll=poll)
                logger.debug(poll_msg)
                if self.verbose:
                    if not polling.is_eual(last_poll, poll):
                        self.print(poll_msg)

                # Checking breakout criteria
                # --------------------------
                if len(reducer.tasks_returned) == len(tasks):
                    logger.debug("All tasks returned.")
                    break

                elif (
                    len(jobs["pending"]) == 0
                    and len(jobs["running"]) == 0
                    and len(jobs["error"]) == 0
                ):
                    logger.warning(
                        "Expected jobs to be either in "
                        "'running', 'pending' or 'error' "
                        "while not all tasks have returned yet."
                    )

                # Not all tasks have returned yet.
                # Prepare to sleep until nex poll
                # --------------------------------
                last_poll = copy.deepcopy(poll)
                time.sleep(self.polling_interval)

            logger.debug("Waiting for tasks to return: done.")

            ## FINISHING
            ## =========
            logger.debug("Closing files to reduce results...")
            reducer.reduce_remaining_stdout_and_stderr_in_case_tasks_did_not_return()

        logger.debug("Closing files to reduce results: done.")

        # Finding out if the work_dir should be removed
        # ---------------------------------------------
        remove_this_work_dir = True

        if self.keep_work_dir:
            logger.debug("User wants to keep work_dir.")
            remove_this_work_dir = False

        if len(reducer.tasks_returned) != len(tasks):
            logger.warning("Not all tasks have returned, will keep work_dir.")
            remove_this_work_dir = False

        if len(reducer.tasks_exceptions) > 0:
            logger.warning("Found exceptions, will keep work_dir.")
            remove_this_work_dir = False

        if len(reducer.tasks_with_stderr) > 0:
            logger.warning("Found non empty stderr, will keep work_dir.")
            remove_this_work_dir = False

        # Reading task results into memory
        # --------------------------------
        logger.debug("Reading results to return them...")
        task_results = reducing.read_task_results(
            work_dir=work_dir,
            len_tasks=len(tasks),
            logger=logger,
        )
        logger.debug("Reading results to return them: done.")

        # shutting down logger
        # --------------------
        logger.debug("Shuting down logger.")
        general_utils.shutdown_logger(logger=logger)
        del logger

        if remove_this_work_dir:
            shutil.rmtree(work_dir)

        return task_results

    def starmap(self, func, iterable, chunksize=None):
        """
        Like map() except that the elements of the iterable are expected
        to be iterables that are unpacked as arguments.
        """
        tasks = [task for task in iterable]
        return self.map(
            func=func,
            iterable=tasks,
            chunksize=chunksize,
            _unpack_task_with_asterisk=True,
        )

    def resubmit_jobs_which_indicate_errors_and_might_profit_from_a_resubmission(
        self,
        num_resubmissions_by_array_task_id,
        work_dir,
        jobname,
        logger,
    ):
        opj = os.path.join
        _jobs = calling.squeue(
            squeue_path=self.squeue_path,
            jobname=jobname,
            array=True,
            timeout=self.slurm_call_timeout,
            logger=logger,
            debug_dump_path=opj(work_dir, "squeue.stdout.dump"),
        )

        jobs = {}
        (
            jobs["running"],
            jobs["pending"],
            jobs["error"],
        ) = organizing_jobs.split_jobs_in_running_pending_error(
            jobs=_jobs, logger=logger
        )

        if len(jobs["error"]) > 0:
            for job in jobs["error"]:
                calling.scancel(
                    scancel_path=self.scancel_path,
                    jobid=job["jobid"],
                    timeout=self.slurm_call_timeout,
                    logger=logger,
                )

            array_task_ids_to_be_resubmitted = []
            for job in jobs["error"]:
                if utils.array_task_shall_be_resubmitted(
                    array_task_id=job["array_task_id"],
                    num_resubmissions_by_array_task_id=num_resubmissions_by_array_task_id,
                    max_num_resubmissions=self.max_num_resubmissions,
                ):
                    array_task_ids_to_be_resubmitted.append(
                        job["array_task_id"]
                    )

            logger.debug("Calling sbatch --array...")
            calling.sbatch(
                script_path=opj(work_dir, "script.py"),
                stdout_path=opj(work_dir, "%a.stdout"),
                stderr_path=opj(work_dir, "%a.stderr"),
                jobname=jobname,
                array=True,
                array_task_ids=array_task_ids_to_be_resubmitted,
                array_num_simultaneously_running_tasks=self.num_simultaneously_running_tasks,
                logger=logger,
                sbatch_path=self.sbatch_path,
                timeout=self.slurm_call_timeout,
            )
            logger.debug("Calling sbatch --array: done.")

            for job in jobs["error"]:
                general_utils.dict_increment(
                    num_resubmissions_by_array_task_id,
                    key=job["array_task_id"],
                )

        num_path = opj(work_dir, "num_resubmissions_by_array_task_id.json")
        with rename_after_writing.open(num_path, "wt") as jf:
            jf.write(json.dumps(num_resubmissions_by_array_task_id))

        return num_resubmissions_by_array_task_id, jobs
