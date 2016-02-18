from ngadnap.dependency_graph.graph import CommandNode 

class TestCommandNode:

    def test_create_command_node(self):
        c = CommandNode("echo hello", "1")
        assert(str(c) == "1")
        assert(c.command == "echo hello")
        c.set_runnable(True)
        assert(c.dependency_free())
