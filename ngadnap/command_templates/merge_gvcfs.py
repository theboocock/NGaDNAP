HAPLOTYPE_CALLER = """
    java -jar {0} \
    {1} \
    -T HaplotypeCaller \
    --emitRefConfidence GVCF
    -R {2} \
    -o {3} \
    --variant_index_type LINEAR \
    --variant_index_parameter 128000 \
    --sample_ploidy {4}
"""

