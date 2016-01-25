# Assignment 3 for OMS6250
#
# Defines a Topology, which is a collection of Nodes. Students should not
# modify this file.  This is NOT a topology like the ones defined in Mininet projects.
#
# Copyright 2015 Sean Donovan

from DistanceVector import *

class Topology(object):

    def __init__(self, conf_file):
        ''' Initializes the topology. Called from outside of DistanceVector.py '''
        self.topodict = {}
        self.nodes = []
        self.topo_from_conf_file(conf_file)
    
    def topo_from_conf_file(self, conf_file):
        ''' This created all the nodes in the Topology  from the configuration
            file passed into __init__(). Can throw an exception if there is a
            problem with the config file. '''
        try:
            conf = __import__(conf_file)
            for key in conf.topo.keys():
                new_node = DistanceVector(key, self, conf.topo[key])
                self.nodes.append(new_node)
                self.topodict[key] = new_node
                
        except:
            print "error importing conf_file " + conf_file
            raise

        self.verify_topo()

    def verify_topo(self):
        ''' Once the topology is imported, we verify the topology to make sure
            it is actually valid. '''
        print self.topodict

        for node in self.nodes:
            try:
                node.verify_neighbors()
            except:
                print "error with neighbors of " + node.name
                raise

    def run_topo(self):
        ''' This is where most of the action happens. First, we have to "prime 
        the pump" and send to each neighbor that they are connected. 

        Next, in a loop, we go through all of the nodes in the topology running
        their instances of Bellman-Ford, passing and receiving messages, until 
        there are no further messages to service. Each loop, print out the 
        distances after the loop instance. After the full loop, check to see if 
        we're finished (all queues are empty).
        '''
        #Prime the pump
        for node in self.nodes:
            node.send_initial_messages()


        done = False
        while done == False:
            for node in self.nodes:
                node.process_BF()
                node.log_distances()
            

            # Done with a round. Now, we call finish_round() which writes out
            # each entry in log_distances(). By default, this will will print 
            # out alphabetical order, which you can turn off so the logfile 
            # matches what is printed during log_distances().
            finish_round()

            done = True
            for node in self.nodes:
                if len(node) != 0:
                    done = False
                    break
