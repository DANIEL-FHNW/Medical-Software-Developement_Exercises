import csv
from collections import Counter
import hashlib

filepath = "/Users/daniel/Desktop/FHNW/Medical Software Developement/CD28_datasets/ncbi_dataset/data/gene.fna"

#NIH_URL_FASTA = "https://www.ncbi.nlm.nih.gov/gene/940"

def open_fasta_file(filepath):
    with open(filepath, 'rt', encoding='utf-8') as f:
        fasta_data = f.read()
    return fasta_data

def gc_content(fasta_data):
    total_bases = len(fasta_data)
    g_count = fasta_data.count('G')
    c_count = fasta_data.count('C')
    gc_percentage = (g_count + c_count) / total_bases * 100
    return gc_percentage

print(f"GC Content: {gc_content(open_fasta_file(filepath)):.2f}%")


