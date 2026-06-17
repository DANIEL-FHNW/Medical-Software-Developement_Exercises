import streamlit as st

st.title("🧬 GC-Content Calculator")

def gc_content(input_sequence):
    if not input_sequence:
        return 0.0
    ##remove the header
    clean_seq = "".join(line for line in input_sequence.splitlines() if not line.startswith(">"))
    clean_seq = clean_seq.upper().replace(" ", "").strip()
    
    if len(clean_seq) == 0:
        return 0.0

    total_bases = len(clean_seq)
    #### total GC-count == ((G + C )/ total bases)) * 100
    gc_count = clean_seq.count('G') + clean_seq.count('C')
    return (gc_count / total_bases) * 100

##text area
st.subheader("Option 1: Enter a sequence manually")
user_input = st.text_area("Sequence:", height=150)

if user_input:
    result_manual = gc_content(user_input)
    st.metric(label="Manual Input GC Content", value=f"{result_manual:.2f}%")

##FASTA-FILE
st.subheader("Option 2: FASTA-File Upload (.fasta, .fa, .txt)")
uploaded_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa", "txt"])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode('utf-8')
    
    # extract header for information
    lines = file_content.splitlines()
    header = "Unbekannte Sequenz"
    
    if lines and lines[0].startswith('>'):
        header = lines[0][1:].strip() # deletes `>`and whitespaces
    
    #gc-content
    result_file = gc_content(file_content)
    #app
    st.success(f"Datei erfolgreich geladen: {uploaded_file.name}")
    
    #name of sequence
    st.markdown(f"**Sequenz-Info:** `{header}`")
    
    st.metric(label="GC-Gehalt", value=f"{result_file:.2f}%")

