"""
    BWA command templates.

    @author James Boocock
"""

import os

# bwa mem -M -t 1 <reference> <fastq1> <fastq2> #  
__BWA_NOT_ANCIENT__="""
    {0} mem -M -t 1 {2} {3} {4} 
"""

# bwa aln -n -o -l <reference> <fq>  
__BWA_ALN__="""
    {0} aln -t 1 -n {1} -o {2} -l {3} {4} {5}
"""
__BWA_ALN_NO_SEED__="""
    {0} aln -t 1 -n {1} -o {2} {3} {4}
"""

# bwa sampe <ref> <sai1> <sai2> <fastq1> <fastq2>
__BWA_SAMPE__="""
    {0} sampe {1} {2} {3} {4} {5}
"""

# bwa samse <ref> <sai> <fastq>
__BWA_SAMSE__="""
    {0} samse {1} {2} {3} 
"""

from ngadnap.dependency_graph.graph import CommandNode

def bwa_samse(args, config, sai, fq):
    """
        Single-ended read processing for bwa
    """
    reference = config['reference']['fasta']
    cmd = __BWA_SAMSE__.format(config['bwa']['executable'],
                               reference, sai, fq)
    id_string = os.path.basename(fq) + ".samse"
    stdout_output = os.path.basename(fq) + ".sam" 
    return CommandNode(cmd, id_string, stdout_output, args.temp_directory)

def bwa_sampe(args, config, sai1, sai2, fq1, fq2):
    """
        Paired-end sample processing.
    """
    reference = config['reference']['fasta']
    cmd = __BWA_SAMPE__.format(config['bwa']['executable'],
                               reference, sai1, sai2,
                               fq1, fq2)
    id_string = os.path.basename(fq1) + ".samse"
    stdout_output = os.path.basename(fq1) + ".sam"
    return CommandNode(cmd, id_string, stdout_output, args.temp_directory)

def bwa_aln(args, config, fq):
    """
        Aln algorithm 
    """
    seeding_off = args.bwa_seeding
    reference = config['reference']['fasta']
    if seeding_off:
        cmd = __BWA_ALN__.format(config['bwa']['executable'], args.bwa_edit_distance, args.bwa_gap_opens, '1024', reference, fq)
    else:
        cmd = __BWA_ALN_NO_SEED__.format(config['bwa']['executable'], args.bwa_edit_distance, args.bwa_gap_opens, reference, fq) 
    id_string = os.path.basename(fq) + 'aln'
    stdout_output = os.path.basename(fq) + '.sai'
    return CommandNode(cmd, id_string, stdout_output, args.temp_directory)

