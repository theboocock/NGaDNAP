from collections import defaultdict
import sys

from ngadnap.exceptions.error_codes import * 

class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed

    def add_connection(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

class CommandNode(object):
    """
        Represents a job (node) for running in a command graph 
    """
    def __init__(self, command_string, id_string): 
        self._command = command_string 
        self._id = id_string
        self._run = False
        self._success = False
        self._can_run = False

    def __str__(self):
        return self._id
    
    @property
    def command(self):
        return self._command
    @property 
    def dependency_free(self):
        return self._can_run

    def run_job(self):
        if self._can_run:
            self.job_queue.add_command(self)
            # Add to job running queue
            

    def set_runnable(self, run_var):
        self._can_run = run_var
        self.run_job()

    def update_node(self, run, success):
        self._run = run
        self._success = success

class CommandGraph(Graph):
    """
        Graph data structure for representing big list of jobs. 
    """
    def __init__(self, job_queue):
        super(CommandGraph, self).__init__(self,directed=True)
        
    def add_node(self, command_node, depends_on):
        """
            Adds node to directed graph
        """
        if type(depends_on) is not list:
            logging.error("Could not add node as parent set was not a list")
            sys.exit(FAILED_ADDING_COMMAND_NODE)
        for temp_depends in depends_on: 
            super(CommandGraph, self).add(self, str(temp_depends), (command_node))

    def update(self, job, success):
        """
            Update jobs status 
        """
        # Mark parent as complete and so then search for new avaliable jobs to run
        if success:
            job.update_node_success(True)
            # get list of new jobs that can be run.
        else:
            logging.error("Job failed to run correctly check log for more information")
