#!/usr/bin/env python3
import sys
import json
import datetime
from pypoolparty import sun_grid_engine

queue_state_path = None  #  <- REQUIRED

# dummy qdel
# ==========
assert len(sys.argv) == 2
JB_job_number = sys.argv[1]

with open(queue_state_path, "rt") as f:
    old_state = json.loads(f.read())

found = False
state = {
    "jobs": [],
    "evil_jobs": old_state["evil_jobs"],
}
for job in old_state["jobs"]:
    if job["JB_job_number"] == JB_job_number:
        found = True
    else:
        state["jobs"].append(job)

with open(queue_state_path, "wt") as f:
    f.write(json.dumps(state, indent=4))

if found == True:
    sys.exit(0)
else:
    print("Can not find ", JB_job_number)
    sys.exit(1)
