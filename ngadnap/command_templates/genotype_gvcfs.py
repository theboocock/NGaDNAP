"""
    GenotypeGVCFs command in the GATK
    {0} : Path to GATK
    {1} : List of BAM files
    {2} : Reference genome
    {3} : VCF output file
"""

GENOTYPEGVCFS_TEMPLATE = """
    java -Djava.io.tmpdir=tmpdir -jar {0} \
    {1} \
    -T GenotypeGVCFs \
    -R {2} \
    -o {3} \
"""

