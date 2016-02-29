# Utility functions for bioinformatics processing
#
# @date 13 Jan 2016
# 

import os
import logging


def __is_exe__(fpath):
    """ 
        Return true if the path is a file and the executable bit is set
    """
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def __is_file__(fpath):
    """ 
        Return true if the path is a file
    """
    return os.path.isfile(fpath)

def which(program, program_name):
    """ 
        Checks whether the file exists on the path or the system path
    """
    program = os.path.expanduser(program)
    fpath = os.path.dirname(program)
    if fpath:
        if __is_exe__(program):
            return True 
        elif __is_file__(program):
            return True 
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if __is_exe__(exe_file):
                return True
    logging.error(program_name + " path = " + fpath +
                 " not locatable in the path of directory specified")
    return False 





