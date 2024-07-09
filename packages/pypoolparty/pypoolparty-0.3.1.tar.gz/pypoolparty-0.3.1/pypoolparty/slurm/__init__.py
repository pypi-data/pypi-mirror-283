from . import array
from . import testing
from . import calling
from . import organizing_jobs
from .. import proto_pool
from .. import utils


@utils.add_doc(
    proto_pool.Pool.__init__.__doc__
    + """sbatch_path : str
            Path to the 'sbatch' executable used to submit jobs.
        clusters : (list of str) or None
            List of the clusters to submit to. See '--clusters' in 'sbatch'.
        squeue_path : str
            Path to the 'squeue' executable used to query the state of jobs.
        scancel_path : str
            Path to the 'scancel' executable used to delete/remove jobs.
    """
    + proto_pool._doc_retrun_statement()
)
def Pool(
    num_chunks=None,
    python_path=None,
    polling_interval=5.0,
    work_dir=None,
    keep_work_dir=False,
    max_num_resubmissions=10,
    verbose=False,
    # slurm specific
    # --------------
    sbatch_path="sbatch",
    clusters=None,
    squeue_path="squeue",
    scancel_path="scancel",
):
    return proto_pool.Pool(
        num_chunks=num_chunks,
        python_path=python_path,
        polling_interval=polling_interval,
        work_dir=work_dir,
        keep_work_dir=keep_work_dir,
        max_num_resubmissions=max_num_resubmissions,
        verbose=verbose,
        submit_func=submit,
        submit_func_kwargs={
            "sbatch_path": sbatch_path,
            "clusters": clusters,
        },
        status_func=status,
        status_func_kwargs={
            "squeue_path": squeue_path,
        },
        delete_func=delete,
        delete_func_kwargs={"scancel_path": scancel_path},
        filter_stderr_func=filter_stderr,
    )


def submit(
    jobname,
    script_path,
    script_arguments,
    stdout_path,
    stderr_path,
    logger,
    # slurm specific
    # --------------
    sbatch_path="sbatch",
    clusters=None,
):
    return calling.sbatch(
        script_path=script_path,
        script_arguments=script_arguments,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        jobname=jobname,
        logger=logger,
        clusters=clusters,
        sbatch_path=sbatch_path,
    )


def status(
    jobnames,
    logger,
    # slurm specific
    # --------------
    squeue_path,
):
    all_jobs = calling.squeue(
        squeue_path=squeue_path,
        logger=logger,
    )
    our_jobs = organizing_jobs.filter_jobs_by_jobnames(
        jobs=all_jobs,
        jobnames=jobnames,
    )
    (
        running,
        pending,
        error,
    ) = organizing_jobs.split_jobs_in_running_pending_error(
        jobs=our_jobs,
        logger=logger,
    )
    out = {
        "running": [],
        "pending": [],
        "error": [],
    }
    for job in running:
        out["running"].append(_make_job(slurm_job=job))
    for job in pending:
        out["pending"].append(_make_job(slurm_job=job))
    for job in error:
        out["error"].append(_make_job(slurm_job=job))
    return out


def delete(
    job,
    logger,
    # slurm specific
    # --------------
    scancel_path,
):
    return calling.scancel(
        jobname=job["name"],
        scancel_path=scancel_path,
        logger=logger,
    )


def _make_job(slurm_job):
    return {
        "name": slurm_job["name"],
    }


def filter_stderr(stderr):
    """
    Remove slurm-foo from job's stderr which can apparently be ignored.

    example
    -------
        '''
        slurmstepd: error: *** JOB 123456 STEPD TERMINATED ON node12 AT
        1846-03-28T02:04:23 DUE TO JOB NOT ENDING WITH SIGNALS ***
        '''
        and
        '''
        slurmstepd: error: slurm_get_node_energy: Socket timed out on send/recv operation
        slurmstepd: error: _get_joules_task: can't get info from slurmd
        '''
    """
    ends_with_newline = False
    if len(stderr) > 0:
        ends_with_newline = stderr[-1] == "\n"

    slurm_foos = [
        "DUE TO JOB NOT ENDING WITH SIGNALS",
        "slurm_get_node_energy: Socket timed out on send/recv operation",
        "_get_joules_task: can't get info from slurmd",
    ]

    lines = str.splitlines(stderr)
    out = []
    for line in lines:
        line_contains_slurm_foo = False

        if "slurmstepd: error:" in line:
            for slurm_foo in slurm_foos:
                if slurm_foo in line:
                    line_contains_slurm_foo = True

        if not line_contains_slurm_foo:
            out.append(line)

    out = str.join("\n", out)
    if ends_with_newline:
        out += "\n"
    return out
