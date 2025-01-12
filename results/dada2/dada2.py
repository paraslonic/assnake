import yaml

rule dada2_filter_and_trim:
    input: 
        r1 = '{prefix}/{df}/reads/{preproc}/{sample}/{sample}_R1.fastq.gz',
        r2 = '{prefix}/{df}/reads/{preproc}/{sample}/{sample}_R2.fastq.gz',
        params = os.path.join(config['assnake_db'], 'params/dada2/filter_and_trim/{params}.yaml')
    output:
        r1 = '{prefix}/{df}/reads/{preproc}__dada2fat_{params}/{sample}/{sample}_R1.fastq.gz',
        r2 = '{prefix}/{df}/reads/{preproc}__dada2fat_{params}/{sample}/{sample}_R2.fastq.gz'
    log: '{prefix}/{df}/reads/{preproc}__dada2fat_{params}/{sample}/{sample}.log'
    conda: 'dada2.yaml'
    wrapper: "file:///data6/bio/TFM/pipeline/assnake/results/dada2/filter_trim_wrapper.py"

rule dada2_learn_errors:
    input: 
        samples_list = os.path.join(config['dada2_dir'], '{sample_set}', 'samples.tsv')
    output:
        err   = os.path.join(config['dada2_dir'], '{sample_set}/err{strand}.rds')
    log: os.path.join(config['dada2_dir'], '{sample_set}/err{strand}.log')
    conda: 'dada2.yaml'
    shell: ('''export LANG=en_US.UTF-8;\nexport LC_ALL=en_US.UTF-8;\n
        Rscript  /data6/bio/TFM/pipeline/assnake/results/dada2/scripts/learn_errors.R '{input.samples_list}' '{output.err}' '{wildcards.strand}' > {log} 2>&1''')

rule dada2_derep_dada_merge:
    input: 
        r1     = '{prefix}/{df}/reads/{preproc}/{sample}/{sample}_R1.fastq.gz',
        r2     = '{prefix}/{df}/reads/{preproc}/{sample}/{sample}_R2.fastq.gz',
        errF   = os.path.join(config['dada2_dir'], '{sample_set}/errR1.rds'),
        errR   = os.path.join(config['dada2_dir'], '{sample_set}/errR2.rds')
    output:
        merged = '{prefix}/{df}/reads/{preproc}/{sample}/{sample}__{sample_set}.merged.rds',
    log: '{prefix}/{df}/reads/{preproc}/{sample}/{sample}__{sample_set}.log'
    conda: 'dada2.yaml'
    shell: ('''export LANG=en_US.UTF-8;\nexport LC_ALL=en_US.UTF-8;\n
        Rscript  /data6/bio/TFM/pipeline/assnake/results/dada2/scripts/derep_dada_merge.R '{input.r1}' '{input.r2}' '{input.errF}' '{input.errR}' '{output.merged}' 12 >{log} 2>&1''')