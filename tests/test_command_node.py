from ngadnap.dependency_graph.graph import CommandNode 
from Queue import Queue

class TestCommandNode:

    def test_create_command_node(self):
        q = Queue()
        c = CommandNode("echo hello", "1", q)
        assert(str(c)=="1")
        assert(c.command == "echo hello")
        c.run_job()
        c.set_runnable(True) 
        c.run_job()
        assert False
