from setuptools import setup, find_packages
import os 

def locate_packages():
    packages = ['ngadnap']
    for (dirpath, dirnames, _) in os.walk(packages[0]):
        for dirname in dirnames:
            package = os.path.join(dirpath, dirname).replace(os.sep, ".")
            packages.append(package)
    return packages

setup(
    name="ngadnap",
    version="1.0",
    packages=locate_packages(),
    author="James Boocock",
    author_email="james.boocock@otago.ac.nz",
    description="Next-generation ancient DNA pipeline",
    license="MIT",
    zip_safe=False,
    url="github.com/smilefreak/NGaDNAP",
    entry_points={
    'console_scripts': [
        'run_ngadnap = ngadnap.pipeline:main',
    ]
    },
    use_2to3=True,
)
