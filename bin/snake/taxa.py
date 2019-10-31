METAPHLAN2 = config['METAPHLAN2']
MPA_PKL = config['MetaPhlAn2']['mpa_v20_m200']
BOWTIE2DB = config['MetaPhlAn2']['BOWTIE2DB']
BOWTIE2 = config['bowtie2.bin']

CENTRIFUGE_FOLDER = config["centrifuge"]["bin"]
CENTRIFUGE_INDEX = config["centrifuge"]["index"]

rule kraken2:
    input:
        r1 = 'datasets/{df}/reads/{preproc}/{sample}/{sample}_R1.fastq.gz',
        r2 = 'datasets/{df}/reads/{preproc}/{sample}/{sample}_R2.fastq.gz'
    output:
        report = 'datasets/{df}/taxa/{preproc}/kraken2/{sample}/report.tsv' # ff param is for FinfFungi
    threads:  12
    run:
        KRAKEN = config["kraken"][str(2)]
        shell ('''{KRAKEN} -ba -t {threads} \
         -o $(basename {output}) \
          -i1 {input.r1} -i2 {input.r2}''')

rule kraken:
    input:
        r1 = 'datasets/{df}/reads/{preproc}/{sample}/{sample}_R1.fastq.gz',
        r2 = 'datasets/{df}/reads/{preproc}/{sample}/{sample}_R2.fastq.gz'
    output:
        report = 'datasets/{df}/taxa/{preproc}/kraken-{version}-ff/{db}/{sample}/report.tsv', # ff param is for FinfFungi
    params:
        classified = 'datasets/{df}/taxa/{preproc}/kraken-{version}-ff/{db}/{sample}/classified.tsv',
        unclassified = 'datasets/{df}/taxa/{preproc}/kraken-{version}-ff/{db}/{sample}/unclassified.tsv',
    threads:  12
    run:
        DB = config['kraken']['db'][str(wildcards.db)]
        KRAKEN = config["kraken"][str(wildcards.version)]
        shell ('''{KRAKEN} --db {DB} --threads {threads} \
         --preload \
         --output {output.report} \
         --classified-out {params.classified} \
         --fastq-input --gzip-compressed {input.r1} {input.r2}''')
