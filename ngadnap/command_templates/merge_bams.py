"""
    
    Merge bam files with the same ReadGroup

"""

__MERGE_BAMS__ = """
    {0}/merge_bams.py -d .  
"""

def merge_bams(args, config, bam_file1, bam_file2):
    """
        Merge all the bam files together.  
    """
    bam_prefix = bam_file1.split('bam')[0] 
    bam_out_name = bam_prefix + '.merged.bam'

    cmd = __MERGE_BAMS__.format(conig['scripts_dir']['directory'])

