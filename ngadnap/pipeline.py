"""
    Date: 29 Feburary 2016 
    Author: James Boocock
    Description: Main NGaDNAP script. 
"""
import argparse
try:
    import ConfigParser
except: 
    import configparser as ConfigParser
import logging
import os
import sys
from ngadnap.create_ngadnap_graph import CreateNGaDNAPGraph 
from ngadnap.dependency_graph.job_queue import JobQueue
from ngadnap.__version__ import __VERSION__ 
from ngadnap.check_paths import check_paths
from ngadnap.utils.environment import set_environment 

def parse_config(args):
    """ Parse config file

        Reads a config and parses the
        arguments into a dictionary.
    """
    config = ConfigParser.ConfigParser()
    config.read(args.config_file)
    config_parsed = {}
    for section in config.sections():
        opts = config.options(section)
        config_parsed[section] = {}
        for op in opts:
            try:
                config_parsed[section][op] = config.get(section, op)
            except:
                logging.info("exception on {0}".format(op))
                config_parsed[section][op] = None
    return config_parsed


def parse_arguments():
    """ 
        Parse all the comandline arguments for the ancient DNA pipeline.
    """
    parser = argparse.ArgumentParser(description="Options for the ancient DNA pipeline")
    adapt_remove = parser.add_argument_group('AdapterRemoval')
    alignment = parser.add_argument_group('Alignment')
    sample_qc = parser.add_argument_group("Sample QC")
    ancient_filter = parser.add_argument_group('Ancient Filtering')
    variant_calling = parser.add_argument_group('Variant Calling')
    vcf_qc = parser.add_argument_group("VCF QC")
    parser.add_argument('-l','--log-file', dest="log_file", default="pipeline_run.log", 
                        help="Log file for the ancient DNA pipeline")
    parser.add_argument("-a","--ancient-dna", dest="ancient_dna",
                        help="Ancient or modern DNA", action="store_true", default=True) 
    parser.add_argument('--use-map-damage', dest="no_map_damage", action="store_false", default=True) 
    parser.add_argument("fastq_files", nargs="*",help="Unzipped fastq files in the following format \
                        <SAMPLEID>.*.R1.fastq <SAMPLEID>.*.R2.fastq") 
    parser.add_argument('-c','--config-file', dest="config_file", 
                        help="Path to configuration file", default="/etc/ancient_dna_pipeline.cfg")
    parser.add_argument('-v', '--verbose',
                        action="store_true", dest='verbose', default=False,
                        help="Verbose command output useful for debugging")
    parser.add_argument("--version", dest="version", help="Print program version",                  
                        action="store_true", default=False)
    parser.add_argument('-d', '--directory', dest="running_directory",
                        help="Directory where the output file should be placed")
    parser.add_argument("-t", "--temp-directory", dest="temp_directory", help="Temporary directory", default="tmp_dir")
    parser.add_argument("-b", "--library-type", dest="library_type", help="Type of Sequencing library: args are double-stranded (ds) and single-stranded (ss)")
    parser.add_argument("--imputation", dest="imputation", help="Perform BEAGLE imputation of the VCF file",
                        default=False, action="store_true")
    parser.add_argument("-m","--use-merged_reads", help="Use the unmergable reads",
                        dest="use_unmerged_reads", action="store_true", default=True)
    adapt_remove.add_argument('--minimum-length',help="Minimum read length to process for analysis",
                             dest="adapt_min_length", default=25)
    adapt_remove.add_argument('--minimum-quality', help="Minimum base quality",
                             dest="adapt_min_qual", default=20)
    adapt_remove.add_argument('--mismatch-rate', help="Mismatch fraction (If >1 set to 1/<mismatch rate>",
                              dest="adapt_mismatch_rate", default=3)
    adapt_remove.add_argument("--min-length", help="Minimum alignment length for merging",
                             dest="adapt_alignment_length", default=11)
    alignment.add_argument("--max-edit-distance", help="Maxmimum edit distance (-n aln)",
                           dest="bwa_edit_distance", default=0.03)
    alignment.add_argument("--max-gap-opens", help="Maximum number of gap opens (-o aln)",
                           dest="bwa_gap_opens", default=2)
    alignment.add_argument("--seeding", help="Should seeding be enabled (disabled by default -l 1024 aln)",
                           dest="bwa_seeding", default=False, action="store_true")
    sample_qc.add_argument("--min-sample-coverage-percent", help="Minimum sample coverage (percentage)", 
                           dest="min_coverage_percent", default=0.95)
    ancient_filter.add_argument('--downweight-number', help="Number of C->T transitions at start and G->A transitions at the end of read to downweight",
                                dest="ancient_downweight_number" ,default="2") 
    variant_calling.add_argument('--min-depth',help="Minimum variant read-depth",
                                dest="vcf_minimum_depth", default=2)
    variant_calling.add_argument('--min-mapping-quality', help="Minimum mapping quality",
                                dest="vcf_min_mapping_quality",default=20)
    args = parser.parse_args()
    if(args.verbose):
        args.level = (logging.DEBUG)
    else:
        args.level = (logging.ERROR)
    if(args.version): 
        logging.info("Version: {0}".format(__version__))
        sys.exit(1)
    if not os.path.isfile(args.config_file):
        logging.info("Could not find config file: {0}".format(args.config_file))
        sys.exit(1)
    return args


def main():
    """ The main function

        Runs the selection pipeline.
    """
    args = parse_arguments()
    config = parse_config(args)
    set_environment(config['environment'])
    logging.basicConfig(format='%(levelname)s   %(asctime)s     %(message)s',
                        filename=args.log_file, filemode='w',
                        level=args.level)
    check_paths(config)
    try:
        cores = int(config['system']['cores_avaliable'])
    except:
        logging.error("Could not read cores_avaliable from the config file")
        # TODO - add real error messages
        sys.exit(1)
    logging.info("Creating Job Queue")
    job_queue = JobQueue(cores)
    logging.info("Success")
    ngadnap_graph = CreateNGaDNAPGraph(args=args, config=config, job_queue=job_queue)
    job_queue.set_command_graph(ngadnap_graph.command_graph)
    ngadnap_graph.populate()
    ngadnap_graph.run()
    print("NGaDNAP ran successfully")
if __name__ == "__main__":
    main()
