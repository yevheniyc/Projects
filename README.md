##Projects
Complete functional projects covering a wide spectrum of topics, including games, bioinformatics, networking,
system/database administration, data science, robotics, machine learning, artificial intelligence, and startup
ideas written in Python, C, SQL, Bash, JavaScript (D3) on various platforms Django, ReactJS, NodeJS, and more.

####SocketIO
This script was written as a response to Wikipedia Research Engineering Team's challenge: 
https://github.com/halfak/research-engineering-task

I handled their challenge with multithreading, but they insisted that multi-processing solution is what they desired. 

Handy script for using Multi-threading with Websockets and Python. I also included their proposed solution (Process_Changes.py), 
but my script can do more work in less time (arguably). 

The main problem here is that threads in Python do NOT achieve true concurrency because of the GIL lock. There are a few tricks to work around it. One of them is to avoid multi-threading all together and use parallism instead with the subprocess module (for example). Another way is to write milti-threading code with synchronization techniques in C and wrap Python around it.

---

####Game
A set of fun games developed with Python and CodeSkulptor for the Coursera's Interactive Programming with Python. 
Implemented basic concepts in mathematics, OOP and graphics to build interactive and dynamic games. Links are provided to "test" the games :)
  1. Pong - implementation of classic ping pong game (don't have too much fun!). Play [here](http://www.codeskulptor.org/#user30_SsWb6yzDfo7EUyz.py)
    - Click on the play button to view game interface
    - Use keyboard arrows: player-1 ('up', 'down') and player-2 ('w', 's')
    - Ball movement will accelerate during the game!
  2. Blackjack - implementation of Blackjack. Please, I don't want your gambling issues on my conscience. Play [here](http://www.codeskulptor.org/#user31_R8PVRLqskziSghE.py)
    - Click on the play button
  3. RiceRocks - spaceships, meteors, lasers, explosions, collisions, acceleration, powerful graphics - no more work for today! [Enjoy here](http://www.codeskulptor.org/#user33_6KEZdn2rEvmOGDF.py)
    - Click on the play button
    - Click "space bar" to shoot
    - Use keyboard arrows for movement

---

####GT_Computer_Networks
Assignments and projects for the Georgia Tech's Computer Networks 6250 Spring 2016 graduate course (OMSCS Program)
  1. Project_1 - Mininet, simple/complex network topologies, network simulation
  2. Project_2 - Mininet, Pyretic, use SDN to build configurable firewall
  3. Project_3 - Distance Vector routing protocol (RIP), shortest paths and Bellman-Ford
  4. Project_4 - Congestion Control, Buffer Bloat, TCP Reno, TCP CUBIC

---

####Evercam API Test
Testing and creating wrappers for Evercam's APIs in Jupyter.

---

####Assay Data Parsers
Data parsers for files generated from different types of assays: ELISA, FACS, Softmax, Biacore/Biacore4000, MSD

---

####Udacity Subtitles Parser
Parser for Udacity's subtitiles zip files.

---

####Multi-threading with C
A set of projects tackling multi-processing, multi-threading, and socket programming with C. 
Topics covered with examples in C are Producer-Consumer models, server/client communication, coditional variables, critical sections, mutaxes and more!

---

####Genomic Data Visualization in Python and Jupyter (to be implemented)
Testing and implementation of the following project at FullStackDatascientist.io: [click here](http://fullstackdatascientist.io/2016-03-15-genomic-data-visualization-using-python/)

Great OOP approach for larger data driven projects.

---
