"""
    Creates a dependency graph that stores the commands for the ancient DNA pipeline.

"""
import os 
import logging

from ngadnap.dependency_graph.graph import CommandGraph, CommandNode
from ngadnap.command_templates.adapter_removal import adapter_removal 
from ngadnap.command_templates.bwa import *
from ngadnap.command_templates.mark_duplicates import *
from ngadnap.command_templates.mapdamage import map_damage, ancient_filter
from ngadnap.command_templates.read_groups import picard_rg

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

    def _populate_gvcfs(self, args, config, bam_dependencies):
        """
            Function to generate the GVCF files. 

            At this point in the process we should have BAM files
            for the entire dataset, we need to extract the sequence            interest from each of the BAM files that survive the an            alysis.
        """

    def _populate_align(self, args, config):
        bam_list = self._get_bam_list(args)
        logging.info("Started populating Alignments Graph")
        reference_genome = config['reference']['fasta']  
        # Do bwa with ancient_options
        align_dependencies = []
        sam_files = {}
        bam_dependencies = []
        for fastqs in bam_list.values():
            fq1 = fastqs[0]
            fq2 = fastqs[1]
            if args.ancient_dna:
                tmp_node1 = adapter_removal(config, args, fq1, fq2)
                #aln
                bwa_node = bwa_aln(args, config, fq1 + '.collapsed')
                self.add_node(bwa_node, [tmp_node1])
               # ##samse1
                bwa_samse1 = bwa_samse(args, config, bwa_node.stdout, fq1 + '.collapsed')
                self.add_node(bwa_samse1, [bwa_node])
               # ##sort sam 
                sam_sort = sort_sam(args, config, bwa_samse1.stdout)
                self.add_node(sam_sort, [bwa_samse1])
               # ##md 
                picard_md_one = picard_md(args,config, sam_sort.stdout) 
                self.add_node(picard_md_one, [sam_sort])
                # rg 
                picard_read_groups = picard_rg(args, config, picard_md_one.stdout)
                self.add_node(picard_read_groups, [picard_md_one])
                # Comment out bam file creation
                if not args.no_map_damage:
                    map_damage_data = map_damage(args, config, picard_md_one.stdout)
                    self.add_node(map_damage_data, [picard_md_one])
                    anc_filter = ancient_filter(args, config, map_damage_data.stdout)
                    self.add_node(anc_filter, [map_damage_data])
                else:
                    anc_filter = ancient_filter(args, config, picard_read_groups.stdout)
                    self.add_node(anc_filter, [picard_read_groups])
                bam_dependencies.append(anc_filter)

                if args.use_unmerged_reads:  
                    bwa_node2 = bwa_aln(args, config, fq1 + '.p1')
                    self.add_node(bwa_node2, [tmp_node1])
                    bwa_node3 = bwa_aln(args, config, fq2 + '.p2')
                    self.add_node(bwa_node3, [tmp_node1])
                    bwa_samse2 = bwa_sampe(args, config, 
                                           bwa_node2.stdout, bwa_node3.stdout,
                                           fq1 + '.p1', fq2 + '.p2')
                    self.add_node(bwa_samse2, [bwa_node2, bwa_node3])
                    sam_sort1= sort_sam(args, config, bwa_samse2.stdout)
                    self.add_node(sam_sort1, [bwa_samse2])
                    filter_unique = filter_unique_bam(args, config, sam_sort1.stdout) 
                    self.add_node(filter_unique, [sam_sort1])
                    picard_read_groups1 = picard_rg(args, config, picard_md_one.stdout)
                    self.add_node(picard_read_groups1, [filter_unique])
                    if not args.no_map_damage:
                        map_damage_data1 = map_damage(args, config, filter_unique.stdout)
                        self.add_node(map_damage_data1, [filter_unique])
                        anc_filter = ancient_filter(args, config, map_damage_data1.stdout)
                        self.add_node(anc_filter, [map_damage_data1])
                    else:
                        anc_filter1 = ancient_filter(args, config, picard_read_groups1.stdout)
                        self.add_node(anc_filter1, [picard_read_groups1])
                    merge_bam = merge_bams(args, config, anc_filter.stdout, anc_filter1.stdout)
                    self.add_node(merge_bam, [anc_filter1, anc_filter])
                    bam_dependencies.append(anc_filter)
                else:
                    bam_dependencies.append()
      #              map_damage_data1 = map_damage(args, config, filter_unique.stdout)
       #             self.add_node(map_damage_data1, [filter_unique])
                    # Mark duplicates
                    # Ancient filter
        return(bam_dependencies)

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
        bam_dependencies = self._populate_align(self.args, self.config)
        self._populate_gvcfs(self.args, self.config, bam_dependencies)

    def run(self):
        self._command_graph.start()
        self._command_graph.finish_block()
    

