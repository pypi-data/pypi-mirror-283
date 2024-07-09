import os
import zipfile
import pickle
import glob
import re
import json
from ... import utils


class Reducer:
    def __init__(self, work_dir):
        zz = zipfile
        self.work_dir = work_dir

        self.results_path = os.path.join(work_dir, "tasks.results.zip")
        self.zip_results = zz.ZipFile(self.results_path + ".part", "w")

        self.stdout_path = os.path.join(work_dir, "tasks.stdout.zip")
        self.zip_stdout = zz.ZipFile(self.stdout_path + ".part", "w")
        self.missing_stdout = set()

        self.stderr_path = os.path.join(work_dir, "tasks.stderr.zip")
        self.zip_stderr = zz.ZipFile(self.stderr_path + ".part", "w")
        self.missing_stderr = set()

        self.exceptions_path = os.path.join(work_dir, "tasks.exceptions.zip")
        self.zip_exceptions = zz.ZipFile(self.exceptions_path + ".part", "w")

        self.tasks_results = []
        self.tasks_exceptions = []
        self.tasks_with_stdout = []
        self.tasks_with_stderr = []

    @property
    def tasks_returned(self):
        return self.tasks_results + self.tasks_exceptions

    def reduce(self):
        result_paths = glob.glob(os.path.join(self.work_dir, "*.pickle"))
        for path in result_paths:
            task_id = get_task_id_from_basename(os.path.basename(path))
            self._reduce_result_of_task(task_id=task_id)
            self.missing_stdout.add(task_id)
            self.missing_stderr.add(task_id)

        exception_paths = glob.glob(os.path.join(self.work_dir, "*.exception"))
        for path in exception_paths:
            task_id = get_task_id_from_basename(os.path.basename(path))
            self._reduce_exception_of_task(task_id=task_id)
            self.missing_stdout.add(task_id)
            self.missing_stderr.add(task_id)

        self._try_reduce_missing_stdout()
        self._try_reduce_missing_stderr()

    def _try_reduce_missing_stdout(self):
        for task_id in list(self.missing_stdout):
            basename = "{:d}.stdout".format(task_id)
            stdout_path = os.path.join(self.work_dir, basename)
            if os.path.exists(stdout_path):
                self._reduce_stdout_of_task(task_id=task_id)
                self.missing_stdout.remove(task_id)

    def _try_reduce_missing_stderr(self):
        for task_id in list(self.missing_stderr):
            basename = "{:d}.stderr".format(task_id)
            stderr_path = os.path.join(self.work_dir, basename)
            if os.path.exists(stderr_path):
                self._reduce_stderr_of_task(task_id=task_id)
                self.missing_stderr.remove(task_id)

    def _reduce_stderr_of_task(self, task_id):
        basename = "{:d}.stderr".format(task_id)
        path = os.path.join(self.work_dir, basename)
        with open(path, "rb") as fin:
            content = fin.read()
            if len(content) > 0:
                self.tasks_with_stderr.append(task_id)
            with self.zip_stderr.open(name=basename, mode="w") as fout:
                fout.write(content)
        os.remove(path)

    def _reduce_stdout_of_task(self, task_id):
        basename = "{:d}.stdout".format(task_id)
        path = os.path.join(self.work_dir, basename)
        with open(path, "rb") as fin:
            content = fin.read()
            if len(content) > 0:
                self.tasks_with_stdout.append(task_id)
            with self.zip_stdout.open(name=basename, mode="w") as fout:
                fout.write(content)
        os.remove(path)

    def _reduce_result_of_task(self, task_id):
        basename = "{:d}.pickle".format(task_id)
        path = os.path.join(self.work_dir, basename)
        with open(path, "rb") as fin:
            with self.zip_results.open(name=basename, mode="w") as fout:
                fout.write(fin.read())
        os.remove(path)
        self.tasks_results.append(task_id)

    def _reduce_exception_of_task(self, task_id):
        basename = "{:d}.exception".format(task_id)
        path = os.path.join(self.work_dir, basename)
        with open(path, "rb") as fin:
            with self.zip_exceptions.open(name=basename, mode="w") as fout:
                fout.write(fin.read())
        os.remove(path)
        self.tasks_exceptions.append(task_id)

    def reduce_remaining_stdout_and_stderr_in_case_tasks_did_not_return(self):
        stdout_paths = glob.glob(os.path.join(self.work_dir, "*.stdout"))
        for path in stdout_paths:
            task_id = get_task_id_from_basename(os.path.basename(path))
            self._reduce_stdout_of_task(task_id=task_id)
        stderr_paths = glob.glob(os.path.join(self.work_dir, "*.stderr"))
        for path in stderr_paths:
            task_id = get_task_id_from_basename(os.path.basename(path))
            self._reduce_stderr_of_task(task_id=task_id)

    def close(self):
        self.zip_results.close()
        self.zip_stdout.close()
        self.zip_stderr.close()
        self.zip_exceptions.close()
        os.rename(self.results_path + ".part", self.results_path)
        os.rename(self.stdout_path + ".part", self.stdout_path)
        os.rename(self.stderr_path + ".part", self.stderr_path)
        os.rename(self.exceptions_path + ".part", self.exceptions_path)
        if self.missing_stdout:
            self._write_json("missing_stdout.json", list(self.missing_stdout))
        if self.missing_stderr:
            self._write_json("missing_stderr.json", list(self.missing_stderr))

    def _write_json(self, basename, obj):
        path = os.path.join(self.work_dir, basename)
        with open(path + ".part", "wt") as f:
            f.write(json.dumps(obj))
        os.rename(path + ".part", path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __repr__(self):
        return "{:s}(work_dir={:s})".format(
            self.__class__.__name__, repr(self.work_dir)
        )


def get_task_id_from_basename(basename):
    return int(re.findall(r"\d+", basename)[0])


def read_task_results_from_zip(path):
    task_results = {}
    with zipfile.ZipFile(path, "r") as zin:
        infos = zin.infolist()
        for info in infos:
            task_id = get_task_id_from_basename(info.filename)
            with zin.open(info.filename, "r") as fin:
                task_result = pickle.loads(fin.read())
                task_results[task_id] = task_result
    return task_results


def read_task_results(work_dir, len_tasks, logger=None):
    logger = utils.make_logger_to_stdout_if_none(logger)

    task_results = read_task_results_from_zip(
        path=os.path.join(work_dir, "tasks.results.zip")
    )
    out = []
    for task_id in range(len_tasks):
        if task_id in task_results:
            out.append(task_results.pop(task_id))
        else:
            out.append(None)
            logger.error("No result found for task_id {:d}.".format(task_id))
    return out
