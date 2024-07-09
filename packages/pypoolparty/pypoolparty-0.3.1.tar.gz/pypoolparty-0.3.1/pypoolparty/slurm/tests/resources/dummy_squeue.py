#!/usr/bin/env python3
import sys
import argparse
import re
import json
import datetime
import subprocess
import pypoolparty

# Every time this is called, it runs one job.
parser = argparse.ArgumentParser(
    description="dummy slurm squeue",
)
parser.add_argument(
    "--me",
    action="store_true",
    required=False,
)
parser.add_argument(
    "--array",
    action="store_true",
    required=False,
)
parser.add_argument(
    "--format", metavar="FORMAT", type=str, required=False, default="%all"
)
parser.add_argument(
    "--name", metavar="JOB_NAME", type=str, required=False, default=""
)
args = parser.parse_args()

queue_state_path = None  #  <- REQUIRED


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def job_head():
    return str.split(job_head_to_line(), "|")


def job_head_to_line():
    return "NAME|JOBID|STATE|REASON|PRIORITY|ARRAY_TASK_ID"


def job_to_line(job, delimiter="|"):
    line = ""
    head = job_head()
    for i, key in enumerate(head):
        line += job[key]
        if (i + 1) < len(head):
            line += "|"
    return line


def state_to_table(state):
    lines = []
    lines.append(job_head_to_line())
    for job in state["jobs"]:
        lines.append(job_to_line(job=job))
    return str.join("\n", lines)


MAX_NUM_RUNNING = 10

with open(queue_state_path, "rt") as f:
    state = json.loads(f.read())

evil_ids_num_fails = {}
evil_ids_max_num_fails = {}
for evil in state["evil_jobs"]:
    if "array_task_id" in evil:
        evil_id = evil["array_task_id"]
    elif "ichunk" in evil:
        assert not args.array, (
            "Expected evil jobs to identify using 'array_task_id'"
            "in case of squeue --array is called."
        )
        evil_id = evil["ichunk"]
    else:
        raise ValueError(
            "Expected evil job to identify itself with either "
            "'ichunk' or 'array_task_id'."
        )

    evil_ids_num_fails[evil_id] = evil["num_fails"]
    evil_ids_max_num_fails[evil_id] = evil["max_num_fails"]


def count_jobs(jobs, state):
    count = 0
    for job in jobs:
        if job["STATE"] == state:
            count += 1
    return count


def find_first_job(jobs, state):
    for i in range(len(jobs)):
        if jobs[i]["STATE"] == state:
            break
    return i


if count_jobs(jobs=state["jobs"], state="RUNNING") >= MAX_NUM_RUNNING:
    run_job = state["jobs"].pop(find_first_job(state["jobs"], "RUNNING"))
    pypoolparty.testing.dummy_run_job(run_job)
elif count_jobs(jobs=state["jobs"], state="PENDING") > 0:
    job = state["jobs"].pop(find_first_job(state["jobs"], "PENDING"))

    # identify evil
    # -------------
    if args.array:
        (
            _,
            evil_id,
        ) = pypoolparty.slurm.array.utils.split_job_id_and_array_task_id(
            job["JOBID"]
        )
    else:
        evil_id = pypoolparty.pooling.make_ichunk_from_jobname(
            jobname=job["NAME"]
        )

    if evil_id in evil_ids_num_fails:
        if evil_ids_num_fails[evil_id] < evil_ids_max_num_fails[evil_id]:
            job["STATE"] = "PENDING"
            job["REASON"] = "err"
            state["jobs"].append(job)
            evil_ids_num_fails[evil_id] += 1
        else:
            job["STATE"] = "RUNNING"
            state["jobs"].append(job)
    else:
        job["STATE"] = "RUNNING"
        state["jobs"].append(job)
elif count_jobs(jobs=state["jobs"], state="RUNNING") > 0:
    run_job = state["jobs"].pop(find_first_job(state["jobs"], "RUNNING"))
    pypoolparty.testing.dummy_run_job(run_job)


evil_jobs = []
for evil_id in evil_ids_num_fails:
    evil_job = {}
    evil_job["num_fails"] = evil_ids_num_fails[evil_id]
    evil_job["max_num_fails"] = evil_ids_max_num_fails[evil_id]
    if args.array:
        evil_job["array_task_id"] = evil_id
    else:
        evil_job["ichunk"] = evil_id

    evil_jobs.append(evil_job)
state["evil_jobs"] = evil_jobs


with open(queue_state_path, "wt") as f:
    f.write(json.dumps(state, indent=4))

out_table = state_to_table(state)
print(out_table)

sys.exit(0)
