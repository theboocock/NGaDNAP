
__MAP_DAMAGE__="""
    {0} -i {1} -d {2} --rescale -r {3} 
"""
import os
from ngadnap.dependency_graph.graph import CommandNode

def map_damage(args, config, bam_file):
    """
        Create the mapdamage command for use in the pipeline 
    """
    bam_prefix = bam_file.split('.bam')[0]
    id_string = bam_prefix +"_filter_unique_bam"
    cmd = __MAP_DAMAGE__.format(os.path.join(config['map_damage']['executable']), bam_file, os.path.abspath(os.path.join(args.temp_directory,bam_prefix)), config['reference']['fasta'])
    bam_out_name = os.path.join(bam_prefix, bam_prefix + '.rescaled.bam') 
    return CommandNode(cmd, id_string, bam_out_name, args.temp_directory)

__ANCIENT_FILTER__="""
    {0}/ancient_filter.py -d {1} --c2t --g2a -i {2} -o {3} -f bam
"""

def ancient_filter(args, config, bam_file):
    """
        Run the ancient filtration procedure 
    """
    bam_prefix = bam_file.split('.bam')[0]
    bam_out_name = bam_prefix  + ".ancient_filter.bam"
    id_string = bam_prefix + "ancient_filter"
    cmd = __ANCIENT_FILTER__.format(config['scripts_dir']['directory'], args.ancient_downweight_number, bam_file, bam_out_name)
    return CommandNode(cmd, id_string, bam_out_name, args.temp_directory)
