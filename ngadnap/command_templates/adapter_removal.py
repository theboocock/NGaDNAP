"""
    Adapter Removal templates
"""

# AdapterRemoval 
#
# {0}: executable
# {1}: fastq1 abs
# {2}: fastq2 abs
# {3}: fastq1 
# {4}: fastq2
# {5}: minimum length
# {6}: mismatch_rate 
# {7}: min base uality
# {8}: min merge_length

__ADAPTER_REMOVAL__="""
     {0} --collapse --file1 {1} --file2 {2} --outputstats {3}.stats --trimns --outputcollapsed {3}.collapsed --minlength {5} --output1 {3}.p1 --output2 {4}.p2 --mm {6} --minquality {7} --minalignmentlength {8} --trimqualities
"""

import os

from ngadnap.dependency_graph.graph import CommandNode 

def adapter_removal(config, args, fq1 ,fq2):
    fq1o = os.path.abspath(fq1)
    fq2o = os.path.abspath(fq2)
    cmd = __ADAPTER_REMOVAL__.format(config['adapter_removal']['executable'], fq1o, fq2o, fq1, fq2, args.adapt_min_length, args.adapt_mismatch_rate ,args.adapt_min_qual, args.adapt_alignment_length)                
    job_id = fq1 + ".adapter_removal" 
    return CommandNode(cmd, job_id, None, args.temp_directory)
