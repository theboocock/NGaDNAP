"""
    Markduplicates for both the merged and unmerged reads.
    
    @author James Boocock
    @date 29 Feb 2016
"""

# 
# {0}: Java
# {1}: Picard jar
# {2}: Input sam
# {3}: 


__PICARD__="""
{0} -jar {1} MarkDuplicates I={2} O={3} M={4} VALIDATION_STRINGENCY=LENIENT 

"""

__PY_SCRIPT__="""
python {0}/filterUniqueBam.py --remove-duplicates {1}
""" 

__SORT__SAM__="""
    {0} -jar {1} SortSam I={2} O={3} SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT 
"""

from ngadnap.dependency_graph.graph import CommandNode 

import os

def sort_sam(args, config, bam_file):
    bam_prefix= bam_file.split('.sam')[0]
    bam_out_name = bam_prefix +".sort.bam"
    id_string = bam_out_name + "_sort_sam"
    cmd=__SORT__SAM__.format(config['java']['executable'], config['picard']['jar'], bam_file, bam_out_name)
    return CommandNode(cmd, id_string, bam_out_name, args.temp_directory)

def picard_md(args, config, bam_file):
    bam_prefix= bam_file.split('.bam')[0]
    bam_out_name = bam_prefix +".md.bam"
    id_string = bam_out_name+ "_picard"
    metrics = bam_prefix + "markdup.txt" 
    cmd=__PICARD__.format(config['java']['executable'], config['picard']['jar'], bam_file, bam_out_name, metrics)
    return CommandNode(cmd, id_string, bam_out_name, args.temp_directory) 

def filter_unique_bam(args, config, bam_file):
    """
        Run filter unique bam script

    """
    bam_prefix= bam_file.split('.bam')[0]
    bam_out_name = bam_prefix +".unique.bam"
    id_string = bam_out_name +"_filter_unique_bam"
    cmd = __PY_SCRIPT__.format(os.path.join(config['scripts_dir']['directory']), bam_file) 
    print id_string
    return CommandNode(cmd, id_string, bam_out_name, args.temp_directory)
