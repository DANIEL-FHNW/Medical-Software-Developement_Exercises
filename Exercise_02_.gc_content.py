import requests

url = "https://www.ncbi.nlm.nih.gov/gene/940/gene.fna"

def open_fasta_from_url(url):
    response = requests.get(url)
    response.raise_for_status() 
    return response.text

def gc_content(fasta_data):
    clean_data = "".join(fasta_data.split()) 
    total_bases = len(clean_data)
    if total_bases == 0:
        return 0

    g_count = clean_data.upper().count('G')
    c_count = clean_data.upper().count('C')
    
    gc_percentage = (g_count + c_count) / total_bases * 100
    return gc_percentage

try:
    data = open_fasta_from_url(url)
    print(f"GC Content: {gc_content(data):.2f}%")
except Exception as e:
    print(f"Failed to process URL: {e}")

