"""
    Testing module for command graph. 

    Simulates a simple job running tree.

"""
import pytest 
from ngadnap.dependency_graph.graph import Graph 

class TestGraph: 

    def test_create_graph(self):
        """
            Create basic graph
        """
        g = Graph()
        assert isinstance(g,Graph)
        assert not g._directed
        g = Graph(True)
        assert isinstance(g,Graph)
        assert g._directed
     
    def test_graph_ops(self):
        g = Graph()
        g.add("n1", "n2")
        g.add("n1", "n4")
        g.add("n2", "n3")
        assert (set(g._graph.keys()) == set(["n1", "n2", "n3", "n4"]))
        assert (set(g.nodes()) == set(["n1", "n2", "n3", "n4"]))
        assert (g._graph['n1'] == set(['n2', 'n4']))
        g = Graph(True)
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




