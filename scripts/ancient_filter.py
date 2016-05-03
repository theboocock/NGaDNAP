#!/usr/bin/env python
#|
#| Downweight bases that are cytosines
#|
#| 
#| Works to perform a C->T transition
#| and a G->A transition
#|
#| @author James Boocock
#| @date 12/09/2014
#|

from Bio import SeqIO
import argparse

def check_c_2_t(base):
    """
        C to T checker
    """
    if base == 'T':
        return True
    else:
        return False

def check_g_2_a(base):
    if base == 'A':
        return True
    else:
        return False

def downweight_quality(quality,change_bases_c=None,change_bases_t=None):
    """
        Returns PHRED qualities that remove downweight Cs or Ts at 
        the start of reads.
    """
    if(change_bases_t and change_bases_c):
        qual_filter=[ a or b for a, b in zip(change_bases_c,change_bases_t)] 
    elif(change_bases_t):
        qual_filter=change_bases_t
    else:
        qual_filter=change_bases_c
    quality=[chr(33 + 0) if filt else q for q, filt in zip(quality,qual_filter)]
    return(quality)

def filter_fastq(input_file,output_file,downweight_number,ctot,gtoa):
    """
        Takes a Fastq file as input and weights the quality of the bases down
        at the start and the end of the reads.

    """
    in_iterator = SeqIO.parse(input_file,'fastq') 
    input_records=list(in_iterator)
    for i, record in enumerate(input_records):
        change_bases_c = None
        change_bases_t = None
        temp_qual = record.letter_annotations['phred_quality']
        if(ctot):
            change_bases_c = [check_c_2_t(nuc) and i < downweight_number for i, nuc in enumerate(record.seq)]
        if(gtoa):
            change_bases_t = [check_g_2_a(nuc) and (len(record.seq)-i) <= downweight_number for i, nuc in enumerate(record.seq)]
        new_qual =downweight_quality(temp_qual, change_bases_c ,change_bases_t) 
        input_records[i].letter_annotations['phred_quality']=new_qual
    handle = file(output_file,'wt')
    SeqIO.write(input_records, handle, "fastq")

import pysam
def filter_bam(input_file, output_file, downweight_number, ctot, gtoa):
    """
        Takes a bam file as input and weights the quality of the reads down.

        Need to ensure we write the header out :)

        Investigate pysam and look for a header,
        this should really help us understand how to get this bam filter working 
        and writing the bam files directly back out to the terminal.
    """
    bam = pysam.Samfile(input_file,'rb')
    bam_out = pysam.Samfile(output_file, 'wb',template=bam) 
    for line in bam:
        change_bases_c = None
        change_bases_t = None
        seq = line.seq
        qual = line.qual
        if(ctot):
            change_bases_c = [check_c_2_t(nuc) and i < downweight_number for i, nuc in enumerate(seq)]
        if(gtoa):
            change_bases_t = [check_g_2_a(nuc) and (len(seq)-i) <= downweight_number for i, nuc in enumerate(seq)]
        new_qual = downweight_quality(qual,change_bases_c, change_bases_t)
        line.qual = new_qual
        bam_out.write(line)
   
        
def main():
    parser = argparse.ArgumentParser(description='Downweight cytosine bases.')
    parser.add_argument('-d','--downweight-number',dest='downweight',help='Downweight', default=int(2))
    parser.add_argument('-c','--c2t',dest='ctot',action='store_true',help='Filter C to T transitions at the start of reads', default=False)
    parser.add_argument('-g','--g2a',dest='gtoa',action='store_true',help='Filter G to A transitions at the end of reads', default=False)
    parser.add_argument('-i','--input-file',dest='input_file',help='Input File - input_fastq' )
    parser.add_argument('-o','--output-file',dest='output_file', help='Output File - out_fastq') 
    parser.add_argument('-f','--format',dest='format', help="File format fastq or bam",default="fastq")
    args = parser.parse_args()
    args.downweight = int(args.downweight)
    assert (args.ctot or args.gtoa), "One of --c2t or g2a needs to be set"
    if (args.format == 'fastq'):
        filter_fastq(args.input_file, args.output_file, args.downweight, args.ctot, args.gtoa)
    elif (args.format == 'bam'):
        filter_bam(args.input_file, args.output_file, args.downweight, args.ctot, args.gtoa)

if __name__ == "__main__":
    main()
