import os
import glob
import importlib
import pandas as pd
configfile: '/data7a/bio/runs-manolov/assnake/config.yml'
include: "/data7a/bio/runs-manolov//assnake/bin/snake/base.py"

fna_db_dir = config['fna_db_dir']
asm_dir = config['assembly_dir']
assnake_db = config['assnake_db']


prefix = '/data10/bio/metagenomics/KazanCrohn/'
samples  = [r.split('/')[-1] for r in glob('/data10/bio/metagenomics/KazanCrohn/reads/raw/*')]
print(samples)

#trim_wc = '/data6/bio/TFM/datasets/kazancrohn/reads/raw__tmtic_def1/{sample}/{sample}_R1.fastq.gz'
mp_wc = '/data10/bio/metagenomics/KazanCrohn/taxa/raw__tmtic_def1/mp2__def/{sample}/{sample}.mp2'
#megahit_wc = os.path.join(asm_dir, 'mh__def/kazancrohn/{sample}/raw__tmtic_def1/final_contigs.fa')

i_want = []

i_want.append(expand(mp_wc, sample=samples))

rule give_me_all:
	input:i_want


