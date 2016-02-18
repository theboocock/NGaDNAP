"""
    Create job queue.

    @date 18 Feb 2016
    @author James Boocock

"""

from ngadnap.utils.run_subprocess import run_subprocess
from ngadnap.exceptions.error_codes import *
from ngadnap.utils.run_subprocess import STOP
try:
    from Queue import Queue
except ImportError:
    from queue import Queue
from threading import Thread
import sys
import logging

def __queue_worker__(q):
    while True:
        queue_item = q.get()
        try:
            # get Api for Queue command etc
            cmd = queue_item[0]
            stdout = queue_item[1]
            stdoutlog = queue_item[2]
            stderr = queue_item[3]
            folder_names = queue_item[4]
            id_string = queue_item[5]
            command = queue_item[6]
            dependency_graph = queue_item[7]
        except IndexError:
            cmd = queue_item[0]
            stdout = queue_item[1]
            stdoutlog = False
            stderr = None
            folder_names = '.'
        try:
            run_subprocess(cmd, id_string, stdout=stdout,
                          stdoutlog=stdoutlog, stderr=stderr,
                          working_dir=folder_names,with_queue=True)
        except SystemExit:
            global STOP
            STOP = True
            logging.error(cmd + ": Failed to run in thread")
        # This needs to be done so we can test the job runner independently
        if dependency_graph is not None:
            dependency_graph.update(command, True)
        q.task_done()


class JobQueue(object):
    """
        Job Queue object. 
    """

    def __init__(self, no_threads=None):
        self._queue = Queue()
        self._no_threads = no_threads
        thread_L = []
        self._command_graph = None
        for i in range(int(no_threads)):
            t = Thread(target=__queue_worker__, args=[self._queue])
            t.daemon = True
            thread_L.append(t)
            t.start()

    def set_command_graph(self, command_graph):
        self._command_graph = command_graph


    def no_jobs(self):
        return len(self._queue)


    def add_job(self, command):
        cmd = command.command
        stdout = command.stdout
        id_string = command.id_string
        stderr = 'stderr_' + id_string + '.tmp' 
        working_dir = command.working_dir
        stdoutlog = False
        if stdout is None:
            stdout_log = True 
        self._queue.put([cmd, stdout, stdoutlog, stderr, working_dir, id_string, command, self._command_graph])
        global STOP 
        if STOP == True:
            sys.exit(SUBPROCESS_FAILED_EXIT)

    def join(self):
        """
            Blocks until the queue is empty  
        """
        return self._queue.join()
