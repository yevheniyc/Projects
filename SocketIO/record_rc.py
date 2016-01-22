"""
Response to Wikipedia challenge. View README.md for a detailed description
of the challenge and approach I've taken.
"""
import time
import json
import random
import sys
import threading
from math import log
import socketIO_client
import stopit

# Keeping thread count and order
# - chose 10 because it accomplished the job
# - more testing could be done with higher numbers
THREADS_MAX = 10
THREADS = []

def process_change(wait_secs):
    """ Sample method, could be used for processing data. 

        Args:
            wait_secs: time to mimick processing time.
    """
    start = time.time()
    while time.time() - start < wait_secs:
        time.sleep(0.001)


class WikiNamespace(socketIO_client.BaseNamespace):

    def on_change(self, change):
        """ Triggered when json data is arriving from the stream and
            contains a "new" or "edit" type.

            Args:
                change: json data describing a stream.
        """
        global THREADS_MAX, THREADS
        # if json's type is new or edit
        if change['type'] in ('new', 'edit'):
            # implement with threading
            for counter in range(THREADS_MAX):
                # generate a different wait time for each thread
                wait = random.lognormvariate(log(1), 1)
                # update json's wait field
                change['wait'] = min(max(wait, 0.01), 10)
                # build the tread
                thread = threading.Thread(target=process_change, 
                                          args=(change['wait'],))
                thread.start()
                # record the sequence
                THREADS.append(thread)
            
            # waiting for threads to finish
            for thread in THREADS:
                thread.join()
                # write out each thread's output keeping json format
                json.dump(change, sys.stdout)
                sys.stdout.write("\n")

            # Reset thread counter for the next round
            THREADS = []

    def on_connect(self):
        """ Sends a "subscribe" message to the indicated server
            when connection has been established
        """
        self.emit('subscribe', 'en.wikipedia.org')  # Subscribes to enwiki

# Create a socket to the specified URL, PORT
socketIO = socketIO_client.SocketIO("stream.wikimedia.org", 80)
# Define a namespace for the /rc requests
socketIO.define(WikiNamespace, '/rc')

# For the next 5 minutes wait for streaming data
with stopit.ThreadingTimeout(5 * 60) as to_ctx_mgr:
    try:
        # wait and receive the incoming stream
        socketIO.wait(10000)
    except KeyboardInterrupt:
        sys.stderr.write("Keyboard interrupt detected.  Shutting down.\n")

# Once all of the threads have been joined and connections complete/interrupted
sys.stderr.write("All done in.\n")