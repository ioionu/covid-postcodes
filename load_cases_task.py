#!/usr/bin/env python3

import procrastinate
import os
import random
import time
import sys

# Make an app in your code
app = procrastinate.App(connector=procrastinate.AiopgConnector(
    user="covid",
    password="covid",
    host="localhost"
))
app.open()

# Then define tasks
@app.task(queue="sum")
def sum(a, b):
    time.sleep(random.random() * 5)
    return a+b

if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    print(f"Scheduling computation of {a} + {b}")
    sum.defer(a=a, b=b)  # This is the line that launches a job

# with app.open():
#     # Launch a job
#     sum.defer(a=3, b=5)

#     # Somewhere in your program, run a worker (actually, it's often a
#     # different program than the one deferring jobs for execution)
#     app.run_worker(queues=["sums"])