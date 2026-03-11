import gzip
import csv
import hashlib
import os
import urllib.request

url = "https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz"
local_path = "gene_info.gz"

# 1. Download
if not os.path.exists(local_path):
    print("Downloading file... this may take a while.")
    urllib.request.urlretrieve(url, local_path)

def get_file_md5(fname):
    hash

filepath = "/https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz"

#MD5-Value
md5_hash = hashlib.md5(filepath.encode('utf-8')).hexdigest()

print(f"MD5 Value: {md5_hash}")

#Open File to read gene information and return a list of dictionaries with tax_id, gene_id, and type_of_gene
def gene_info_opener(filepath, limit=None):
    with open(filepath, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')  
        header = next(reader)                   
        header[0] = header[0].lstrip('#').strip()
                                
        genes = []
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break
            tax_id = row[0]
            gene_id = row[1]
            type_of_gene = row[9]
            genes.append({'tax_id': tax_id, 'gene_id': gene_id, 'type_of_gene': type_of_gene})
    
    return genes


### 1.how many genes are listed?

def how_many_genes(filepath):
    with open(filepath, 'rt', encoding='utf-8') as f:  
        reader = csv.reader(f, delimiter='\t')          
        next(reader)                                    
        return sum(1 for row in reader)                 


print(f"Answer question 1: {how_many_genes(filepath)}") #Total genes: 66396446


### 2. How many genes are listed for the species Homo Sapiens?

def how_many_genes_homo_sapiens(filepath):
    with open(filepath, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        return sum(1 for row in reader if row[0] == '9606')  # tax_id for Homo sapiens is 9606
    

print(f"Answer question 2: {how_many_genes_homo_sapiens(filepath)}") #Total genes for homo sapiens: 193790

### 3. List of all gene types

def all_gene_types(filepath):
    with open(filepath, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        return(list(set(row[9] for row in reader)))
    

print(f"Answer question 3: {all_gene_types(filepath)}")

### 4. Which gene occurs the most?

def most_frequent_gene(filepath):
    with open(filepath, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        gene_counts = Counter(row[9] for row in reader)
    
    gene, count = gene_counts.most_common(1)[0]
    return gene, count

gene, count = most_frequent_gene(filepath)
print(f"Answer question 4: Type {gene} appears {count} times") #protein-coding (appears 52192148 times)
