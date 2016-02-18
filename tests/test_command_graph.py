"""
    Testing python dependency graph for ancient DNA pipeline

    @author James Boocock   
    @date 18 Feb 2016
"""

import pytest

from ngadnap.dependency_graph.graph import CommandNode, CommandGraph, Graph
from ngadnap.dependency_graph.job_queue import JobQueue

import os

class TestCommandGraph:
   

    def test_create_graph(self):
        q = JobQueue(1)
        g = CommandGraph(q)
        g.add("n1", "n2")
        g.add("n1", "n4")
        g.add("n2", "n3")
        assert (set(g._graph.keys())== set(["n1", "n2"]))
        g.remove("n1")
        assert (set(g._graph.keys()) == set(["n2"]))
        g.add("n1", "n4")
        g.remove("n4")
        assert (g._graph['n1'] == set([]))
        assert (g.get_adjacent('n1') == set([]))
        assert (g.get_adjacent('n2') == set(["n3"]))

    def test_basic_depends_on(self):
        q = JobQueue(1)
        g = CommandGraph(q)
        q.set_command_graph(g)
        c1 = CommandNode("sleep 1", "1")
        c2 = CommandNode("echo hello", "2", stdout="test.txt") 
        g.add_node(command_node=c1, depends_on=[c2])
        assert set(g.nodes())== set(['1', '2'])
        g.start()
        g.finish_block()
        os.remove('test.txt')

    def test_two_depends_on(self):
        q = JobQueue(1)
        g = CommandGraph(q)
        q.set_command_graph(g)
        c1 = CommandNode("sleep 1", "1")
        c2 = CommandNode("echo hello", "2", stdout="test.txt") 
        c3 = CommandNode("echo hello", "3", stdout="test2.txt") 
        g.add_node(command_node=c1, depends_on=[c3,c2])
        g.add_node(command_node=c3, depends_on=[c2])
        g.start()
        g.finish_block()
        os.remove("test.txt")
        os.remove("test2.txt")
