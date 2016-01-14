#!/usr/bin/env python
"""
    This program takes a vcf input and converts the VCF
    file to a fasta file containing all the relevant information
    for further analysis. In humans only one such problem exists
    with an indel being called in a different place on the reference
    sequence.


"""
import vcf, argparse, sys
from pyfasta import Fasta

def is_ga_or_ct(ref, alt):
    if len(ref) == 1 and len(alt) == 1:
        alt = alt[0]
        if ref == "C" and alt == "T":
            return True
        elif ref == "T" and alt == "C":
            return True
        elif ref == "G" and alt == "A":
            return True
        elif ref == "A" and alt == "G":
            return True
    else:
        return False


def vcf_to_fasta(input_vcf, output_fasta, ref_seq,
                 species, use_indels, min_depth, free_bayes,
                 ploidy, to_fasta, main_sequence, coverage_files,
                 min_probs=0.8, impute=False, unique_only=False):
    # First part is to get the fasta sequence then atke each position
    # and then alter the reference as necessary for each sample.
    # Because everyone will have different SNPs.
    f = Fasta(ref_seq)
    # For now this is only going to work with mtDNA sequences,
    # but plan to extend this in the future to full genome
    # gets the full genomes sequences and currently assumes
    # that the fasta only contains one sequence.
    min_depth = int(min_depth)
    ploidy = int(ploidy)
    if(impute):
        is_beagle = True
    index = [n for n, l in enumerate(f.keys()) if l.startswith(main_sequence)]
    index = index[0]
    full_sequence = list(str(f[f.keys()[index]]))
    min_max_coord = []
    first_coordinate = True 
    sample_fasta = {}
    unique_snps = {}
    if free_bayes or ploidy == 1:
        free_bayes = True
        ploidy = 1
    if(impute):
        is_beagle = True
        free_bayes = False
    sample_lines = {}
    vcf_reader = vcf.Reader(open(input_vcf, 'r'), strict_whitespace=True)
    samples = vcf_reader.samples
    sample_offset = {}
    sample_offset_end= {}
    for sample in samples:
        sample_lines[sample] = []
        sample_fasta[sample] = full_sequence[:]
        sample_offset[sample] = 0
        sample_offset_end[sample] = {}
    for record in vcf_reader:
        position = record.POS
        if first_coordinate:
            min_max_coord.append(str(position))
            first_coordinate = False
        for sample in record.samples:
            genotype = sample['GT']
            is_beagle = False
            temp_position = position - 1  + sample_offset[sample.sample]
            try:
                pl = sample['PL']
                pheno_l = [int(o) for o in pl]
                dp = sample['DP']
                pl = pheno_l.index(min(pheno_l))
                if genotype == None or float(dp) <= min_depth:
                    sample_fasta[sample.sample][temp_position] = 'N'
                    # Just to ensure, the bad thing doesn't occur
                    # Overwriting the N call.
                    continue
            except AttributeError:
                if not free_bayes:
                    is_beagle = True
                    gp = sample['GP']
                    g_l = [float(o) for o in gp]
                    if max(g_l) < min_probs:
                        #print sample
                        sample_fasta[sample.sample][temp_position] = 'N'
                        continue
                    pl = g_l.index(max(g_l))
                else:
                    if genotype == '.' or genotype == None:
                        sample_fasta[sample.sample][temp_position] = 'N'
                        continue
            except TypeError:
                sample_fasta[sample.sample][temp_position] = 'N'
                continue
            sample = sample.sample
            if free_bayes or ploidy == 1:
                genotype = genotype[0]
                if genotype == '0':
                    continue
            elif not is_beagle:
                genotype = genotype.split('/')
            else:
                genotype = genotype.split("|")
            # If pl is greater than zero
            ref = record.REF
            alt = record.ALT
            # Gl is substituted
            if free_bayes or int(pl) > 0:
                if is_ga_or_ct(ref, alt):
                    if not free_bayes:
                        if is_beagle:
                            if g_l[0] > g_l[2]:
                                continue
                        elif pheno_l[0] < pheno_l[2]:
                            continue
                no_alleles = 1 + len(alt)
                if not free_bayes:
                    genotype = genotype[0]
                real_gt = str(alt[int(genotype)-1])
                if real_gt == "*":
                    sample_fasta[sample][temp_position] = "N"
                    continue
                if to_fasta:
                    if species == 'human':
                        if position == 8270 and ref == "CACCCCCTCT":
                            sample_fasta[sample][8280:8289] = '-'*9
                            continue
                    for i in range(0, max(len(real_gt), len(ref))):
                        if  i == (len(real_gt) - 1) and i == (len(ref)- 1):
                            gt = real_gt[i]
                            if free_bayes and len(str(alt)) > 1:
                                real_gt = str(alt[0])
                            #print(temp_position)
                            sample_fasta[sample][temp_position] = gt
                        elif len(real_gt) > len(ref) and i != 0:
                            if use_indels:
                                gt = list(real_gt[i])
                                sample_offset_end[sample][temp_position] = len(gt)

                                temp_position = temp_position + 1
                                sample_fasta[sample] = \
                                    sample_fasta[sample][:temp_position] + \
                                    gt + sample_fasta[sample][temp_position:]
                                sample_offset[sample] += 1
                            else:
                                gt = real_gt[i]
                                sample_fasta[sample][temp_position] = gt[0]
                        elif len(real_gt) < len(ref) and i != 0:
                            sample_fasta[sample][temp_position + i] = '-'
                else:
                    if species == 'human':
                        if position == 955 and  "ACCCC" in str(alt[0]):
                            sample_lines[sample].extend(["960.1CCCCC"])
                            try:
                                unique_snps["960.1CCCCC"] += 1
                            except KeyError:
                                unique_snps["960.1CCCCC"] = 1
                            continue
                        if position == 8270 and ref == "CACCCCCTCT":
                            sample_lines[sample].extend([str(i)+"d" for i in range(8281, 8290)])
                            for item in [str(i) +"d" for i in range(8281, 8290)]:
                                try:
                                    unique_snps[item] += 1
                                except KeyError:
                                    unique_snps[item] = 1
                            continue
                        if position == 285 and ref == "CAA":
                            sample_lines[sample].extend([str(i) + "d" for i in range(290, 293)])
                            for item in [str(i) +"d" for i in range(290, 293)]:
                                try:
                                    unique_snps[item] += 1
                                except KeyError:
                                    unique_snps[item] = 1
                            continue
                        if position == 247 and ref == "GA":
                            sample_lines[sample].extend([str(249) + "d"])
                            item = str(249) + "d"
                            try:
                                unique_snps[item] += 1
                            except KeyError:
                                unique_snps[item] = 1
                            continue
                    for i in range(0, max(len(real_gt), len(ref))):
                        if i == (len(real_gt) - 1) and i == (len(ref)- 1):
                            gt = real_gt[i]
                            if free_bayes and len(str(alt)) > 1:
                                real_gt = str(alt[0])
                            sample_lines[sample].append(str(position+i) + gt)
                            if unique_only:
                                try:
                                    unique_snps[str(position+i) + gt] += 1
                                except KeyError:
                                    unique_snps[str(position+i) + gt] = 1
                        elif len(real_gt) > len(ref) and i != 0:
                            gt = real_gt[i]
                            sample_lines[sample].append(str(temp_position+i) + "."  + str(i) + gt)
                            if unique_only:
                                try:
                                    unique_snps[str(temp_position+i) + "."  + str(i) + gt] += 1
                                except KeyError:
                                    unique_snps[str(temp_position+i) + "."  + str(i) + gt] = 1
                            temp_position = temp_position - 1

                        elif len(real_gt) < len(ref) and i != 0:
                            sample_lines[sample].append(str(position+i) + "d")
                            if unique_only:
                                try:
                                    unique_snps[str(position+i) + "d"] += 1
                                except KeyError:
                                    unique_snps[str(position+i) + "d"] = 1
    if to_fasta:
        sample_fasta_count_changes = {}
        for sample in samples:
            if not impute:
                for cov in coverage_files:
                    if sample in cov:
                        with open(cov) as coverage_f:
                            start = 0
                            for line in coverage_f:
                                s_line = line.split('\t')
                                start_temp = int(s_line[1]) -1
                                while start_temp != start:
                                    sample_fasta[sample][start] = 'N'
                                    start += 1
                                coverage = int(s_line[3])
                                if coverage <= min_depth:
                                    sample_fasta[sample][start] = 'N'
                                start += 1
            else:
                for cov in coverage_files:
                    if sample in cov:
                        with open(cov) as coverage_f:
                            start = 0
                            for line in coverage_f:
                                s_line = line.split('\t')
                                start_temp = int(s_line[1]) -1
                                while start_temp != start:
                                    try:
                                        sample_fasta_count_changes[start] += 1
                                    except KeyError:
                                        sample_fasta_count_changes[start] = 1
                                    #sample_fasta[sample][start] = 'N'
                                    start += 1
                                coverage = int(s_line[3])
                                if coverage <= min_depth:
                                    try:
                                        sample_fasta_count_changes[start] += 1
                                    except KeyError:
                                        sample_fasta_count_changes[start] = 1
                                    #sample_fasta[sample][start] = 'N'
                                start += 1
            # TODO make sure that this cannot get called when using the indels option
        if impute:
            for sample in samples:
                offset = 0
                for i in range(0,len(sample_fasta[sample])):
                    if i in sample_offset_end[sample]:
                        offset += sample_offset_end[sample][i]    
                    try: 
                        temp_number = sample_fasta_count_changes[i]
                        if temp_number == len(coverage_files):
                            sample_fasta[sample][i+offset] = 'N'
                    except KeyError:
                        pass
        with open(output_fasta, 'w') as out:
            for sample in samples:
                out.write('>'+ sample + '\n')
                out.write("".join(sample_fasta[sample]) + '\n')
    else:
        if unique_only:
            unique_truth = {}
            for snp, count in unique_snps.items():
                if count == len(sample_lines):
                    unique_truth[snp] = False
                else:
                    unique_truth[snp] = True
        min_max_coord.append(str(position))
        with open(output_fasta, 'w') as hgrep_o:
            hgrep_o.write('SampleId\tRange\tHaploGroup\tPolymorphisms (delimited by tab)\n')
            for sample, substitions in sample_lines.items():
                output_line = []
                output_line.append(sample)
                output_line.append('-'.join(min_max_coord))
                output_line.append("?")
                for sub in substitions:
                    if unique_only:
                        if unique_truth[sub] == True:
                            output_line.append(sub)
                    else:
                        output_line.append(sub)
                output_line = "\t".join(output_line) + "\n"
                if len(output_line.split('\t')) == 3:
                    continue
                hgrep_o.write(output_line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--vcf', dest="vcf_input",
                        help="VCF input file to convert to fasta")
    parser.add_argument('-o', '--output', dest="fasta_output",
                        help="Fasta output file")
    parser.add_argument('-r', '--reference', dest='reference',
                        help="Reference FASTA sequence file")
    parser.add_argument('-m', '--main_sequence', dest='main_sequence',
                        help='Main sequence for analysis')
    parser.add_argument('-s', '--species', dest='species', default='human',
                        help="Species that you are performing analysis on, "
                        "Currently accepted values are human and dog")
    parser.add_argument('--use-indels', dest='use_indels', action="store_true",
                        help="Do not use indels in the analysis", default=False)
    parser.add_argument('--min-depth', dest="min_depth",
                        default=0)
    parser.add_argument('--free-bayes', dest='free_bayes', default=False,
                        action="store_true")
    parser.add_argument('--ploidy', dest='ploidy', default=2)
    parser.add_argument('--to-haplo', dest='to_fasta', default=True,
                        action="store_false")
    parser.add_argument('-p', '--impute', dest='impute', default=False,
                        action="store_true")
    parser.add_argument('-u', '--unique_only', dest="unique",
                        default=False, action="store_true")
    parser.add_argument('coverage_files', nargs='*')
    args = parser.parse_args()
    assert  args.fasta_output is not None, \
            "-o or --output is required"
    assert args.vcf_input is not None, \
            "-i or --vcf is required"
    assert args.reference is not None, \
            "-r or --reference is required"
    if args.use_indels is None:
        args.use_indels = False
    if args.main_sequence is None:
        args.main_sequence = "gi|251831106|ref|NC_012920.1| " \
                "Homo sapiens mitochondrion, complete genome"
        if args.species != 'human':
            sys.stderr.write(args.vcf_input)
            sys.stderr.write("Cannot default main sequence on anything but human mtDNA\n")
            sys.exit(1)
    if args.to_fasta and args.unique:
        sys.stderr.write("Cannot run unique on new sequences \n")
        sys.exit(1)
    if (args.to_fasta):
        # Ensure the regex has been expanded, meaning that we actually found files
        if "*" in args.coverage_files[0]:
            sys.stderr.write("Could not find any coverage_files\n")
            args.coverage_files = []
    # TODO Ensure the pipeline script correctly runs this part.
    vcf_to_fasta(args.vcf_input, args.fasta_output, args.reference, 
                 args.species, args.use_indels, args.min_depth,
                 args.free_bayes, args.ploidy, args.to_fasta,
                 args.main_sequence, args.coverage_files,
                 impute=args.impute, unique_only=args.unique) 
if __name__ == "__main__":
    main()

