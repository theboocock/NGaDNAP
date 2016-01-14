# Python Script to perform for running the single process for our pipeline
#
# Murray Cadzow
# July 2013
# University Of Otago
#
# James Boocock
# July 2013
# University Of Otago
#
import argparse
import ConfigParser
import logging
import os
import sys
from .standard_run import StandardRun
from .environment import set_environment
from ._version import __version__
logger = logging.getLogger(__name__)
SUBPROCESS_FAILED_EXIT = 10

def parse_config(args):
    """ Parse config file

        Reads a config and parses the
        arguments into a dictionary.
    """
    config = ConfigParser.ConfigParser()
    config.read(args.config_file)
    config_parsed = {}
    logger.debug(config.sections())
    for section in config.sections():
        logger.debug(section)
        opts = config.args(section)
        config_parsed[section] = {}
        for op in opts:
            logger.debug(op)
            try:
                config_parsed[section][op] = config.get(section, op)
            except:
                logger.info("exception on {0}".format(op))
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
    parser.add_argument('-l','--log-file', "log_file", default="pipeline_run.log", 
                        help="Log file for the ancient DNA pipeline")
    parser.add_argument("fastq_files", help="Unzipped fastq files in the following format \
                        <SAMPLEID>.*.R1.fastq <SAMPLEID>.*.R2.fastq") 
    parser.add_argument('-c','--config-file', dest="config_file", 
                        help="Path to configuration file", default="/etc/ancient_dna_pipeline.cfg")
    parser.add_argument('-v', '--verbose',
                        action="store_true", dest='verbose', default=False,
                        help="Verbose command output useful for debugging")
    parse.add_argument("--version", dest="version", help="Print program version",
                       action="")
    parser.add_argument('-d', '--directory', dest="running_directory",
                        help="Directory where output file should be placed")
    parser.add_argument("-l", "--library-type", dest="library_type", help="Type of Sequencing library: args are double-stranded (ds) and single-stranded (ss)")
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
    alignment.add_argument("--algorithm", help="BWA alignment algorithm (mem or aln)", 
                           dest="bwa_algo", default="aln")
    alignment.add_argument("--max-edit-distance", help="Maxmimum edit distance (-n aln)",
                           dest="bwa_edit_distance", default=0.03)
    alignment.add_argument("--max-gap-opens", help="Maximum number of gap opens (-o aln)",
                           dest="bwa_gap_opens", default=2)
    alignment.add_argument("--seeding", help="Should seeding be enabled (disabled by default -l 1024 aln)",
                           dest="bwa_seeding", default=False, action="store_true")
    sample_qc.add_argument("--min-sample-coverage-percent", help="Minimum sample coverage (%)", 
                           dest="min_coverage_percent", default=0.95)
    ancient_filter.add_argument("--rescale-bams", help="Rescale base qualities using mapDamage",
                                dest="ancient_rescale", default=False, action="store_true")
    ancient_filter.add_argument('--downweight-number', help="Number of C->T transitions at start and G->A transitions at the end of read to downweight",dest="ancient_downweight_number" ,default=2) 
    variant_calling.add_argument('--min-depth', dest="Minimum read-depth", help="Minimum variant read-depth",
                                dest="vcf_minimum_depth", default=2)
    variant_calling.add_argument('--min-mapping-quality', help="Minimum mapping quality",
                                dest="vcf_minimum_depth", default=20)
    
    args = parser.parse_args()
    if(args.verbose):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    if(args.ver): 
        logging.info("Version: {0}".format(__version__))
        sys.exit(1)        
    return args


def main():
    """ The main function

        Runs the selection pipeline.
    """
    args = parse_arguments()
    config = parse_config(args)
    set_environment(config['environment'])
    if args.cores is not None:
        config['system']['cores_avaliable'] = args.cores
    logging.basicConfig(format='%(asctime)s     %(message)s',
                        filename=args.log_file, filemode='w',
                        level=logging.INFO)
    s = StandardRun(args, config=config)
    s.run_pipeline()
    print("Selection Pipeline Completed Successfully :)!")

if __name__ == "__main__":
    main()
