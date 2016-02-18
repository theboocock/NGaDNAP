import pytest

from ngadnap.dependency_graph.graph import CommandNode
from ngadnap.dependency_graph.job_queue import JobQueue

import time
import os
class TestJobRunner:
    
    def _create_simple_job(self):
        c = CommandNode("echo hello", "1")
        return(c)

    def test_run_simple_job(self):
        com = self._create_simple_job()
        q = JobQueue(1)
        q.add_job(com)
        q.join()

    def test_run_save_stdout(self):
        os.mkdir("test_dir")     
        c = CommandNode("echo hello", "1", stdout="test.txt", working_dir="test_dir")
        q = JobQueue(1)
        q.add_job(c)
        q.join()
        f = open("test_dir/test.txt").read().strip()
        assert f == "hello"
        os.remove("test_dir/test.txt")
        os.rmdir("test_dir")

    def test_run_multicore_job(self):
        one_hundred_jobs = []
        for i in range(10):
            one_hundred_jobs.append(CommandNode("sleep 1", str(i)))
        com = self._create_simple_job()
        q = JobQueue(10)
        for job in one_hundred_jobs:
            q.add_job(job)
        q.join()
    
