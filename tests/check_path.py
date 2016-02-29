"""
    Testing that the config checker works correctly
"""

import pytest

from ngadnap.pipeline import parse_config 
from ngadnap.check_paths import check_paths 

class Args:
    pass

class TestCheckPaths:

    def _get_config(self):
        args = Args()
        args.config_file = "tests/data/defaults.cfg"
        config = parse_config(args)
        return config

    def test_parse_config(self):
        config = self._get_config()
        assert config['bwa']['executable'] == "bwa" 

    def test_check_paths_simple(self):
        config = self._get_config()
        check_paths(config)
    
