from collections import defaultdict
import sys

from threading import Thread
from time import sleep

import logging

from ngadnap.exceptions.error_codes import * 

class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass
    def nodes(self):
        items = [item for o in self._graph.keys() for item in self._graph[o]]
        keys = list(self._graph.keys())
        keys.extend(items) 
        keys=list(set(keys))
        return(keys)

    def get_adjacent(self, node):
        """
            Extract the adjacent nodes from the graph.
        """
        return(self._graph[node])

class CommandNode(object):
    """
        Represents a job (node) for running in a command graph 
    """
    def __init__(self, command_string, id_string, stdout=None, working_dir=None):
        self._command = command_string
        self._id = id_string
        self._run = False
        self._success = False
        self._stdout = stdout
        self._working_dir = working_dir
 
    def __str__(self):
        return self._id
    @property
    def working_dir(self):
        return self._working_dir

    @property
    def command(self):
        return self._command
    @property
    def id_string(self):
        return self._id
    @property
    def stdout(self):
        return self._stdout
    
    @property 
    def run(self):
        return self._run
    
    @property
    def success(self):
        return self._success
    

    def update_node(self, run, success):
        self._run = run
        self._success = success

class CommandGraph(Graph):
    """
        Graph data structure for representing big list of jobs. 
    """
    def __init__(self, job_queue):
        super(CommandGraph, self).__init__(directed=True)
        self.job_queue = job_queue
        self.node_list = {}

    def add_node(self, command_node, depends_on):
        """
            Adds node to directed graph
        """
        if type(depends_on) is not list:
            logging.error("Could not add node as parent set was not a list")
            sys.exit(FAILED_ADDING_COMMAND_NODE)
        for temp_depends in depends_on: 
            super(CommandGraph, self).add(str(command_node), str(temp_depends))
            self.node_list[str(temp_depends)] = temp_depends
        self.node_list[str(command_node)] = command_node

    def _get_runnable_commands(self):
        commands_to_run = []
        nodes = list(self.node_list.keys())
        for node in nodes:
            node_obj = self.node_list[node]
            if node_obj.run != True:
                adjacent_nodes = self.get_adjacent(node)
                total_success = 0
                for adj in adjacent_nodes:
                    adj = self.node_list[adj]
                    if adj.success:
                        total_success += 1 
                if total_success == len(adjacent_nodes): 
                    commands_to_run.append(node)
        return commands_to_run 

        

    def _send_new_commands(self):
        """
            Add's new jobs to the command to enable further processing.
        """
        new_commands = self._get_runnable_commands()
        for command in new_commands:
            self.node_list[command].update_node(True, False)
            self.job_queue.add_job(self.node_list[command])

    def _finished(self):
        # Check that the job queue has not died
        self.job_queue
        nodes = super(CommandGraph, self).nodes()
        successes = sum([self.node_list[node].success for node in self.node_list.keys()])
        if successes == len(nodes):
            return True
        else:
            return False

    def finish_block(self):
        """
            Method to call and block until
            the end of the method.
        """
        while True:
            finished = self._finished()
            if finished:
                break
            else:
                sleep(1)


    def start(self):
        self._send_new_commands()

    def update(self, command, success):
        """
            Update command status and check whether all commands are complete 
        """
        # Mark parent as complete and so then search for new avaliable jobs to run
        if success:
            command.update_node(run=True, success=True)
            finished = self._finished()
            if finished:
                logging.info("Pipeline completed successfully !")
                # cleanup pipeline and finished the process
            self._send_new_commands()
            # get list of new jobs that can be run.
        else:
            logging.error("Job failed to run correctly check log for more information")


