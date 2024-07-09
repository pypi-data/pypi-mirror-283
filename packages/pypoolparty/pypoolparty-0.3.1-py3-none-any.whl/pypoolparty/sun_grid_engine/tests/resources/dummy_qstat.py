#!/usr/bin/env python3
import sys
import json
import datetime
import subprocess
import pypoolparty

queue_state_path = None  #  <- REQUIRED


def job_to_xml(job):
    jld = ""
    jld += '<job_list state="{:s}">\n'.format(job["@state"])
    jld += "    <JB_job_number>{:s}</JB_job_number>\n".format(
        job["JB_job_number"]
    )
    jld += "    <JAT_prio>{:s}</JAT_prio>\n".format(job["JAT_prio"])
    jld += "    <JB_name>{:s}</JB_name>\n".format(job["JB_name"])
    jld += "    <JB_owner>{:s}</JB_owner>\n".format(job["JB_owner"])
    jld += "    <state>{:s}</state>\n".format(job["state"])
    jld += "    <JB_submission_time>{:s}</JB_submission_time>\n".format(
        job["JB_submission_time"]
    )
    jld += "    <queue_name>{:s}</queue_name>\n".format(job["queue_name"])
    jld += "    <slots>{:s}</slots>\n".format(job["slots"])
    jld += "</job_list>\n"
    return jld


def state_to_xml(state):
    out_xml = "<?xml version='1.0'?>\n"
    out_xml += "<job_info>\n"

    out_xml += "    <queue_info>\n"
    for job in state["jobs"]:
        if job["@state"] == "running":
            out_xml += indent_text(job_to_xml(job), indent=8)
    out_xml += "    </queue_info>\n"

    out_xml += "    <job_info>\n"
    for job in state["jobs"]:
        if job["@state"] != "running":
            out_xml += indent_text(job_to_xml(job), indent=8)
    out_xml += "    </job_info>\n"

    out_xml += "</job_info>\n"
    return out_xml


def indent_text(text, indent=4):
    out = []
    spaces = " " * indent
    for line in text.splitlines():
        out.append(spaces + line + "\n")
    return "".join(out)


# dummy qstat
# ===========
# Every time this is called, it runs one job.
MAX_NUM_RUNNING = 10

assert len(sys.argv) == 2
assert sys.argv[1] == "-xml"

with open(queue_state_path, "rt") as f:
    state = json.loads(f.read())

evil_ichunks_num_fails = {}
evil_ichunks_max_num_fails = {}
for evil in state["evil_jobs"]:
    evil_ichunks_num_fails[evil["ichunk"]] = evil["num_fails"]
    evil_ichunks_max_num_fails[evil["ichunk"]] = evil["max_num_fails"]


def count_jobs(jobs, state):
    count = 0
    for job in jobs:
        if job["@state"] == state:
            count += 1
    return count


def find_first_job(jobs, state):
    for i in range(len(jobs)):
        if jobs[i]["@state"] == state:
            break
    return i


if count_jobs(state["jobs"], "running") >= MAX_NUM_RUNNING:
    run_job = state["jobs"].pop(find_first_job(state["jobs"], "running"))
    pypoolparty.testing.dummy_run_job(run_job)
elif count_jobs(state["jobs"], "pending") > 0:
    job = state["jobs"].pop(find_first_job(state["jobs"], "pending"))
    ichunk = pypoolparty.pooling.make_ichunk_from_jobname(
        jobname=job["JB_name"]
    )
    if ichunk in evil_ichunks_num_fails:
        if evil_ichunks_num_fails[ichunk] < evil_ichunks_max_num_fails[ichunk]:
            job["@state"] = "pending"
            job["state"] = "Eqw"
            state["jobs"].append(job)
            evil_ichunks_num_fails[ichunk] += 1
        else:
            job["@state"] = "running"
            job["state"] = "r"
            state["jobs"].append(job)
    else:
        job["@state"] = "running"
        job["state"] = "r"
        state["jobs"].append(job)
elif count_jobs(state["jobs"], "running") > 0:
    run_job = state["jobs"].pop(find_first_job(state["jobs"], "running"))
    pypoolparty.testing.dummy_run_job(run_job)


evil_jobs = []
for ichunk in evil_ichunks_num_fails:
    evil_jobs.append(
        {
            "ichunk": ichunk,
            "num_fails": evil_ichunks_num_fails[ichunk],
            "max_num_fails": evil_ichunks_max_num_fails[ichunk],
        }
    )
state["evil_jobs"] = evil_jobs


with open(queue_state_path, "wt") as f:
    f.write(json.dumps(state, indent=4))

out_xml = state_to_xml(state)
print(out_xml)

sys.exit(0)
