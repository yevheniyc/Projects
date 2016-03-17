# This script was provided as a desired solution to the challenge. 
# Although, I like mine better, this is a more elegant solution which utilizes ProcessPoolExecutor's
# map function to keep track of the order in which processing tasks come in. I used a simple list to keep track 
# of the threads.  

# The multi-threading solution I've provided is able to handle more processing at the same time, however, 
# if the processing tasks require significant CPU power, the below solution is the way to go!  

import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count


def main():
    # Constructs a streaming generator of change_docs
    change_docs = (json.loads(l) for l in sys.stdin)

    # One processor per CPU
    processing_pool = ProcessPoolExecutor(max_workers=cpu_count())

    # This map() function preserves order using `Future`s internally
    for change_doc in processing_pool.map(process_change_doc, change_docs):
        sys.stderr.write(".")
        sys.stderr.flush()
        json.dump(change_doc, sys.stdout)
        sys.stdout.write("\n")

    sys.stderr.write("\n")
    sys.stderr.flush()


def process_change_doc(change_doc):
    process_change(change_doc['wait'])  # Fake processor
    return change_doc


def process_change(wait_secs):
    start = time.time()
    while time.time() - start < wait_secs:
        time.sleep(0.001)


if __name__ == "__main__":
    main()
