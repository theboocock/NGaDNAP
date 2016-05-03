#!/usr/bin/env python
"""
    Module merges a list a bam file sharing the same read group.

"""

import argparse
import pysam
import os

def get_bam_pairs(bams):
    """
        Function returns pairs of bam files because sample ID relies
        on samples being encoded with a '.'

        @bams  A List of Bam files.
    """
    ### TODO Use the read group to merge the reads, far smarter!
    bam_list = {}
    for bam in bams:
        sam = pysam.AlignmentFile(bam,'rb')
        sample_id = (sam.header['RG'][0]['SM'])
        try:
            bam_list[sample_id].append(bam)
        except KeyError:
            bam_list[sample_id] = [bam]
    return bam_list

def get_header(bam):
    """
        Return the BAM header.
    """
    return pysam.AlignmentFile(bam,'rb').header

def merge_reads(bams, merged_output_dir):
    """
        Merge bam files, can take odd numbers of reads. 
    """
    try:
        os.mkdir(merged_output_dir)
    except OSError:
        pass

    bam_list = get_bam_pairs(bams)
    for sample_id, bams in bam_list.items():
        header = get_header(bams[0])
        bam_out = os.path.join(merged_output_dir, os.path.basename(sample_id)) + '.bam'
        out = pysam.AlignmentFile(bam_out, 'wb', header=header)
        for bam in bams:
            sam = pysam.AlignmentFile(bam, 'rb')
            for read in sam:
                out.write(read)
        out.close()
        pysam.sort(bam_out, 'tmp')
        os.rename('tmp.bam',bam_out)
        pysam.index(bam_out)

def main():
    """
        Processe and merges bams.

    """
    parser = argparse.ArgumentParser(description="Merges bam files by read group")
    parser.add_argument('bams', nargs='2')
    parser.add_argument('-o', '--output-bam', dest='output_bam_file')
    args = parser.parse_args()
    merge_reads(args.bams, args.merged_output_dir)

if __name__ == "__main__":
    main()
