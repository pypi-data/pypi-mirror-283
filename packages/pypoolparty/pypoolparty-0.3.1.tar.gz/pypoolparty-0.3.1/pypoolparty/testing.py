import json
import subprocess
import os
import tempfile
from . import utils


def dummy_init_queue_state(path, evil_jobs=[]):
    qstate = {"jobs": [], "evil_jobs": evil_jobs}
    utils.write_text(path=path, content=json.dumps(qstate))


def dummy_run_job(job):
    if "_additional_environment" in job:
        special_env = os.environ.copy()
        special_env.update(job["_additional_environment"])
    else:
        special_env = None

    with open(job["_opath"], "wt") as o, open(job["_epath"], "wt") as e:
        cmd = [job["_python_path"]]
        if "_script_arg_0" in job:
            cmd += [job["_script_arg_0"]]
        if "_script_arg_1" in job:
            cmd += [job["_script_arg_1"]]
        subprocess.call(cmd, stdout=o, stderr=e, env=special_env)


def read_shebang_path(path):
    txt = utils.read_text(path=path)
    lines = str.splitlines(txt)
    firstline = lines[0]
    assert str.startswith(firstline, "#!")
    return firstline[2:]


class DebugDirectory:
    def __init__(self, debug_dir=None, prefix="", suffix=""):
        if debug_dir:
            self.debug = True
            self.tmp_dir_handle = None
            dirname = prefix + "debug" + suffix
            self.name = os.path.join(debug_dir, dirname)
            os.makedirs(self.name, exist_ok=True)
        else:
            self.debug = False
            self.tmp_dir_handle = tempfile.TemporaryDirectory(
                prefix=prefix, suffix=suffix
            )
            self.name = self.tmp_dir_handle.name

    def cleanup_when_no_debug(self):
        if not self.debug:
            self.tmp_dir_handle.cleanup()

    def __enter__(self):
        return self.name

    def __exit__(self, type, value, traceback):
        self.cleanup_when_no_debug()

    def __repr__(self):
        return self.__class__.__name__ + "()"
