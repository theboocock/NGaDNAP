"""
    Creates a dependency graph that stores the commands for the ancient DNA pipeline.

"""
import os 
import logging

from ngadnap.dependency_graph.graph import CommandGraph, CommandNode
from ngadnap.command_templates.adapter_removal import adapter_removal 
from ngadnap.command_templates.bwa import *

class CreateNGaDNAPGraph(object):
    """
        Represents NGADNAGRaph.

        Processes the command-line options and arguments 
        to generate a custom command graph that will then be run. 
    """

    def _get_bam_list(self, args):
        fastq_pairs = {}
        for fastq in args.fastq_files:
            sample = fastq.split('.')[0]
            # Will this get us to the first dot or _ where the sample name is specified
            sample = sample.split('_')[0]
            try:
                fastq_pairs[sample].append(fastq)
            except KeyError:
                fastq_pairs[sample] = [fastq]
        return fastq_pairs

    def add_node(self, node, dependencies): 
        """
            Add node to the command graph
        """
        self._command_graph.add_node(command_node=node, depends_on=dependencies)

    def _populate_graph(self, args, config):
        bam_list = self._get_bam_list(args)
        logging.info("Started populating Job Graph")
        reference_genome = config['reference']['fasta']  
        # Do bwa with ancient_options
        align_dependencies = []
        sam_files = {}
        for fastqs in bam_list.values():
            fq1 = fastqs[0]
            fq2 = fastqs[1]
            if args.ancient_dna:
                tmp_node1 = adapter_removal(config, args, fq1, fq2)
                bwa_node = bwa_aln(args, config, fq1 + '.collapsed')
                self.add_node(bwa_node, [tmp_node1])
                bwa_samse1 = bwa_samse(args, config, bwa_node.stdout, fq1 + '.collapsed') 
                self.add_node(bwa_samse1, [bwa_node])
                picard_md_one = picard_md(args,config, bwa_samse1.stdout)
                # Add node
                self.add_node(picard_md_one, [bwa_node])
                
                if args.use_unmerged_reads:  
                    bwa_node2 = bwa_aln(args, config, fq1 + '.p1')
                    self.add_node(bwa_node2, [tmp_node1])
                    bwa_node3= bwa_aln(args, config, fq2 + '.p2')
                    self.add_node(bwa_node3, [tmp_node1])
                    bwa_samse2 = bwa_sampe(args, config, 
                                           bwa_node2.stdout, bwa_node3.stdout,
                                           fq1 + '.p1', fq2 + '.p2')
                
                    # Mark duplicates 
                    # Rescale if needed
                # Then create the dependencies between bwa and adapter, don't need dependencies for the other jobs.
       
    @property
    def command_graph(self):
        return self._command_graph

    def __init__(self, args, config, job_queue):
        try:
            os.mkdir(args.temp_directory)
        except:
            pass
        self._job_queue = job_queue 
        self._command_graph = CommandGraph(job_queue)
        self.args = args 
        self.config = config 

    def populate(self):
        self._populate_graph(self.args, self.config)

    def run(self):
        self._command_graph.start()
        self._command_graph.finish_block()
    
    def bwa(self, fastqs, ancient=False):
        """
            Creates the BWA command-line for both ancient and non-ancient runs.
        """
        ids = []
        if ancient:
            return None
        else:
            return None

    

