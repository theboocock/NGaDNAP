import os
import signal
import argparse
import sys
import subprocess
import shlex
from threading import Thread
from threading import Lock
from time import sleep
import logging
STOP=False

log_writer = Lock()

from ngadnap.exceptions.error_codes import *

def run_subprocess(
    command, tool, stdout=None,
    stderr=None, stdoutlog=False,
        working_dir=None,with_queue=False):
    """ Runs a command on the system shell and forks a new process
        also creates a file for stderr and stdout if needed
        to avoid deadlock.
    """
    command = shlex.split(command)
    logging.info(tool + " preparing to run " + ' '.join(command))
    if (working_dir is None):
        working_dir = '.'
    else:
        if stdout is not None:
            stdout = os.path.join(working_dir, stdout)  
#    if(tool == 'selection_pipeline'):
 #       stderr = working_dir+'/selection_stderr.tmp'
  #      stdout = working_dir+ '/selection_stdout.tmp'
    if(stderr is None):
        stderr = 'stderr.tmp'
        standard_err = open(stderr, 'w')
    else:
        standard_err = open(stderr, 'w')
    try:
        if(stdout is None):
            standard_out_file = "stdout_" + tool + ".tmp" 
            if working_dir != ".":
                standard_out_file = os.path.join(working_dir,"stdout_" + tool + ".tmp")
            standard_out = open(standard_out_file, 'w')
            exit_code = subprocess.Popen(
                command, stderr=standard_out, stdout=standard_err,cwd=working_dir)
        else:
        # find out what kind of exception to try here
            if(hasattr(stdout, 'read')):
                exit_code = subprocess.Popen(
                    command, stdout=stdout, stderr=standard_err,cwd=working_dir)
            else:
                stdout = open(stdout, 'w')
                exit_code = subprocess.Popen(
                    command, stdout=stdout, stderr=standard_err, cwd=working_dir)
            standard_out = stdout
    except:
        logging.error(tool + " failed to run " + ' '.join(command))
        standard_err = open(stderr, 'r')
        with log_writer:
            while True:
                line = standard_err.readline()
                if not line:
                    break
                logging.info(tool + " STDERR: " + line.strip())
            standard_err.close()
            sys.exit(SUBPROCESS_FAILED_EXIT)
    try:
        while(exit_code.poll() is None):
            sleep(0.2)
            if(STOP == True):
                exit_code.send_signal(signal.SIGINT) 
                if with_queue:
                   return
                else:
                    sys.exit(SUBPROCESS_FAILED_EXIT)
    except (KeyboardInterrupt, SystemExit):
        exit_code.send_signal(signal.SIGINT) 
        global STOP
        STOP = True
        if with_queue:
            return
        else:
            sys.exit(SUBPROCESS_FAILED_EXIT)
    standard_err.close()
    standard_out.close()
    standard_err = open(stderr, 'r')
    if(exit_code.returncode != 0):
        logging.error(tool + " failed to run " + ' '.join(command))
        with log_writer:
            while True:
                line = standard_err.readline()
                if not line:
                    break
                logging.info(tool + " STDERR: " + line.strip())
            sys.exit(SUBPROCESS_FAILED_EXIT)
    stdout_log = False
    if(stdout is None):
        standard_out = open(standard_out_file, 'r')
        stdout_log = True
    elif(stdoutlog):
        if(hasattr(stdout, 'write')):
            standard_out = open(stdout.name, 'r')
        else:
            standard_out = open(stdout, 'r')
        stdout_log = True
    if(stdout_log):
        with log_writer:
            while True:
                line = standard_out.readline()
                if not line:
                    break
                logging.info(tool + " STDOUT: " + line.strip())
            standard_out.close()
    with log_writer:
        while True:
            line = standard_err.readline()
            if not line:
                break
            logging.info(tool + " STDERR: " + line.strip())
    logging.info("Finished tool " + tool)
    logging.debug("command = " + ' '.join(command))
    standard_err.close()
    standard_out.close()
    # Removed stdout if it either was not specified
    # or the log was specified.
    if(stdout is None):
        os.remove(standard_out_file)
    elif(stdoutlog):
        os.remove(standard_out.name)
    os.remove(stderr)
