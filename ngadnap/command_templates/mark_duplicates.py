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
{0} -jar {1} I={2} O={3} M={4}
"""

__PY_SCRIPT__="""
{0}/filterUniqueBam.py {1}
""" 

from ngadnap.dependency_graph.graph import CommandNode 

def picard_md(args, config, bam_file):
    bam_prefix= bam_file.split('.bam')[0]
    bam_out_name = bam_prefix +".md.bam"
    id_string = bam_out_name+ "_picard"
    metrics = bam_prefix + "markdup.txt" 
    cmd=__PICARD__.format(config['java']['executable'], config['picard']['jar'], bam_file, bam_out_name, metrics)
    return CommandNode(cmd, id_string, bam_out_name, args.temp_directory) 

def filter_unique_bam(args, config):
    return None
