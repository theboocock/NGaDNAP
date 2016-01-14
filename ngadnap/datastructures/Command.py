class Command(object):
    """
        Represents a command in a abstract sense. 
    """
    
    def __init__(self, command_string, name):   
        self.command = command_string
        self.name = name
    @property
    def command(self):
        return self.command
    @property
    def name(self):
        return self.name



