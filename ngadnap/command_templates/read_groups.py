"""
    Picard Read groups

"""

__READ__GROUPS__="""
    {0} -jar {1} AddOrReplaceReadGroups I={2} O={3}  VALIDATION_STRINGENCY=LENIENT RGPL={4} RGPU={4} RGSM={4} RGLB={4}
"""

from ngadnap.dependency_graph.graph import CommandNode

def picard_rg(args, config, bam_file):
    sample_id = bam_file.split('_')[0]
    bam_out_name = bam_file.split('.bam')[0] + ".rg.bam"
    id_string = bam_out_name + "_rg_bam"
    cmd = __READ__GROUPS__.format(config['java']['executable'], config['picard']['jar'], bam_file, bam_out_name, sample_id)
    return CommandNode(cmd, id_string, bam_out_name, args.temp_directory)
