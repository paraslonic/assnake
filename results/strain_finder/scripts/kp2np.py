import numpy as np
import argparse, glob, re, sys
import _pickle as cPickle


# Merge kpileups from multiple samples. Write dictionary of (M, N, 4) numpy arrays where:
# M = samples
# N = alignment sites
# 4 = nucleotides (ACGT)
# Entry (i,j,k) of this array corresponds to the count of nucleotide k at position j of sample i

# Read input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--samples', nargs='+', help='Sample list (newline-delimited)')
parser.add_argument('--gene_file', help='kpileup gene file')
parser.add_argument('--out', help='Output file (.cPickle)')
args = parser.parse_args()

samples = []
for s in args.samples:
    samples.append(s.split('/')[-2])
print(samples)

# Initialize data
nts = 'ACGT'

# Map samples to indices
sample2index = {}
i = 0
for s in samples:
    sample2index[s] = i
    i += 1
print(sample2index)
M = len(sample2index)

# Initialize numpy arrays for each genome
x = {}
for line in open(args.gene_file):
    line = line.rstrip().split()
    contig = line[0]
    beg = int(line[2])
    end = int(line[3])
    x[contig] = np.zeros([M, end, 4])

# Add kpileup results to numpy arrays
for sample in args.samples:
    for line in open(sample):
        line = line.rstrip().split()
        if len(line) == 10 and line[0] != 'Sample':
            sample = line[0]
            i = sample2index[sample]
            contig = line[1]
            j = int(line[2])
            nt = line[7]
            k = nts.index(nt)
            count = int(line[8])
            x[contig][i,j-1,k] = count

# Write numpy arrays to file
cPickle.dump(x, open(args.out, 'wb'))