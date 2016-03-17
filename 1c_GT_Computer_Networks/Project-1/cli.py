#!/usr/bin/python

"Networking Assignment 1"

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

from complextopo import ComplexTopo

def latencyTest():
    "Create network and run latency test"
    topo = ComplexTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    #print "Testing network latency"

    CLI(net)

    #net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('output')
    latencyTest()
