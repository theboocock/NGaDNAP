"""
    Testing module for command graph. 

    Simulates a simple job running tree.

"""
import pytest 
from ngadnap.dependency_graph.graph import Graph, CommandGraph, CommandNode

class TestGraph: 

    def test_create_graph(self):
        g = Graph()
        print(g)
        assert False 

