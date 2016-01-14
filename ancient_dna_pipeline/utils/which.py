# Utility functions for bioinformatics processing
#
# @date 13 Jan 2016
# 

import logging

logging = logging.getLogger(__name__)

def which(program, program_name):
    """ Checks whether the file exists on the path or the system path
    """
    fpath, fname = os.path.split(program)
    if fpath:
        if __is_exe__(program):
            return program
        elif (__is_script__(program)):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if __is_exe__(exe_file):
                return exe_file
    logger.error(program_name + " path = " + fpath +
                 " not locatable in the path of directory specified")
    return None





