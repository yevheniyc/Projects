# Assignment 3 for OMS6250
#
# This defines a Node that can fun the Bellman-Ford algorithm. Students
# should not modify this file, but should instead modify the DistanceVector
# class that inherits from Node.
#
# Copyright 2015 Sean Donovan

class Node(object):

    def __init__(self, name, topolink, neighbors):
    # name is the name of the local node
    # links is a list of all neighbors's names. 
    # topology is a backlink to the Topology class. Used for accessing neighbors
    #   as follows: self.topology.topodict['A']
    # messages is a list of pending messages from neighbors to be processed.
    #   The format of the message is up to you; a tuple will work.
        self.name = name
        self.links = neighbors
        self.topology = topolink
        self.messages = []

    def __len__(self):
        ''' Returns the length of the message queue. '''
        return len(self.messages)

    def __str__(self):
        ''' Returns a string representation of the node. '''

        retstr = self.name + " : links ( "
        for neighbor in self.links:
            retstr = retstr + neighbor + " "
        return retstr + ")"
        

    def __repr__(self):
        return self.__str__()

        

    def verify_neighbors(self):
        ''' Verify that all your neighbors has a backlink to you. '''
        for neighbor in self.links:
            if self.name not in self.topology.topodict[neighbor].links:
                raise Exception(neighbor + " does not have link to " + self.name)

    def send_msg(self, msg, dest):
        ''' Performs the send operation, after verifying that the neighber is
            valid.
        '''
        if dest not in self.links:
            raise Exception("Neighbor " + dest + " not part of neighbors of " + self.name)
        
        self.topology.topodict[dest].queue_msg(msg)
        

    def queue_msg(self, msg):
        ''' Allows neighbors running Bellman-Ford to send you a message, to be
            processed next time through self.process_BF(). '''
        self.messages.append(msg)
