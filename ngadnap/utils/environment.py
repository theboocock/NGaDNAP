#
# Append to environment variables.
#

import os

def set_environment(environment_variables):
    for environ, value in environment_variables.items():
        environ = environ.upper()
        if(environ in os.environ):
            os.environ[environ] += (":" + value)
        else:
            os.environ[environ] = value
