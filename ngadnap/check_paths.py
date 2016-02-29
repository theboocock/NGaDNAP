"""
    Parses the check_paths options

    @date 29 Feb 2016
"""

from ngadnap.utils.which import which, __is_file__

def check_paths(config):
    """
        Need to make sure all the paths in the config file exist in the folders they are expected to. 
    """
    assert which(config['bwa']['executable'], "bwa")
    assert which(config['samtools']['executable'], "samtools")
    assert which(config['java']['executable'], "java")
    assert which(config['muscle']['executable'], "muscle")
    assert which(config['seqmagick']['executable'], "seqmagick")
    assert which(config['reference']['fasta'], "reference")
    assert which(config['adapter_removal']['executable'], "adapter_removal")

