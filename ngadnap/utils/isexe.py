
def __is_exe__(fpath):
    """ Return true if the path is a file and the executable bit is set
    """
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
