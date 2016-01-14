from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name="NGaDNAP",
    version="1.0",
    packages=['ancient_dna_pipeline'],
    author="James Boocock",
    author_email="james.boocock@otago.ac.nz",
    description="Next-generation ancient DNA pipeline",
    license="MIT",
    zip_safe=False,
    url="github.com/smilefreak/ancient_dna_pipeline",
    use_2to3=True,
)
