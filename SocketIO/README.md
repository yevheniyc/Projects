####Handling Wiki* edits with SocketIO and threading.
***

NOTE: Code specifically processes the incomming RCStream from stream.wikimedia.org, not the hardcoded dummy data mentioned in the chellenge at: https://github.com/halfak/research-engineering-task

1. Default socketIO-client installs socket.io protocol 1.x, whereas RCStream runs on 0.9.
   To fix, manually install 0.5.6:
   ```
   >> pip install https://pypi.python.org/packages/source/s/socketIO-client/socketIO-client-0.5.6.tar.gz
   ```
2. Review information:
    - Review concurrency, threads, sockets, web sockets: 
        - Gevent library: http://learn-gevent-socketio.readthedocs.org/en/latest/general_concepts.html
        - Python sockets overview: https://docs.python.org/2/howto/sockets.html
        - SocketIO-client API: https://pypi.python.org/pypi/socketIO-client/0.5.6
    - Read and understand the provided material and suggested links
    - Read over RCStream API
    - Read over SocketIO API

3. Design and architecture:
    - Understand the provided code: comment
    - Test the provided code and run it locally
    - Implement and test process_change(wait_secs) function without threading
    - Add multi-threading  

4. Resoning behind threading:
    - The objective is to 
        - process the incoming RCStream data faster than implemented by each stream's processing algorithm.
        - the order of incomming streams must stay intact during output.
    - The provided process_change(wait_secs) function, therefore, needs to be executed concurrently,
      so that in a specified amount of time (5 mins) more than 5 mins worth of processing could be done.
    - To execute the processing function concurrently, multiple-threads were used
    - To keep track of the threads order, a global THREADS list is used. Each time thread is started, it is added to the list.
      After threads in the list have been joined, the list is emptied and thread generation continues. 
    - After multiple tests, 10 concurrent threads were enough to significantly increase efficiency of processing data (i.e ~200 seconds worth
      of processing was done in 60 seconds)

5. Next Steps and Design Flaws:
    - I tested thread order and efficiency of the multi-threading using a timer, could be viewd in the commits, however, I did not have
      time to write proper tests. 
    - The next step would be to implement the threads not only concurrently, but also in parallel using multiple processes.  
