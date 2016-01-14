"""
    py.test module. 
    
    Used for testing included vcf_to_fasta script.

"""
import pytest

class TestVCFToFasta:
    
    def test_create_directory(self, tmpdir):
        print(tmpdir)
        assert True
