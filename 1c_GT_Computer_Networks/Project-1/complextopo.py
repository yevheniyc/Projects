"""
complextopo.py - Yevheniy Chuba - 01/24/2016

Mimiking complex network topologies with Mininet.
The following link configurations allow to mimic 
the following links:

	     Bandwidth(Mbps)    Delay(ms)    Loss Rate(%)		
   Ethernet:       20  		1		0
   WiFi: 	   10		   3		   3
   3G: 		   2		   10		   10
"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom

# Topology to be instantiated in Mininet
class ComplexTopo(Topo):
	"""Mininet Complex Topology:
	
		h1-(ethernet)-s1-(ethernet)-s2-(ethernet)-s3-(wifi)-h2
					    |
					 (ethernet)
					    |
					    s4
					    |
					   (3G)
					    |
					    h3
	"""

	def __init__(self, cpu=.1, max_queue_size=None, **params):

		# Initialize topo
		Topo.__init__(self, **params)

		# Host and link configuration
		hostConfig = {'cpu': cpu}
		ethernetConfig = {'bw': 20, 'delay': '1ms', 'loss': 0,
						  'max_queue_size': max_queue_size} 
		wifiConfig = {'bw': 10, 'delay': '3ms', 'loss': 3,
					  'max_queue_size': max_queue_size}
		threegConfig = {'bw': 2, 'delay': '10ms', 'loss': 10,
						'max_queue_size': max_queue_size}

		# Hosts and switches - mininet
		h1 = self.addHost('h1', **hostConfig)
		h2 = self.addHost('h2', **hostConfig)
		h3 = self.addHost('h3', **hostConfig)

		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')

		# different types of links - mininet
		self.addLink(h1, s1, **ethernetConfig)
		self.addLink(s1, s2, **ethernetConfig)
		self.addLink(s2, s3, **ethernetConfig)
		self.addLink(s2, s4, **ethernetConfig)
		self.addLink(s3, h2, **wifiConfig)
		self.addLink(s4, h3, **threegConfig)
