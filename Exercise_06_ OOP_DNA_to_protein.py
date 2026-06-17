from Bio.Seq import Seq


#2. store sequence into an object of class SequenceStorage
#   - SequenceStorage is a singleton class: onlys 1 object
class SequenceStorage:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SequenceStorage, cls).__new__(cls)
            cls._instance.data = {}
        return cls._instance

    def save(self, name, seq):
        self.data[name] = seq

    def read(self, name):
        return self.data.get(name)


class ProteinStorage(SequenceStorage):
    _instance = None                      

    AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

    def _is_valid(self, seq):
        return all(c in self.AMINO_ACIDS for c in str(seq).upper())

    def save(self, name, seq):           
        if not self._is_valid(seq):
            raise ValueError(f"Invalid protein sequence: {seq}")
        super().save(name, seq)


# create a DNA/protein sequence "factory" which creates Biopython Seq objects based on a flag
#create_sequence == BioPython with raw sequence and sequence type
class SequenceFactory:

    @staticmethod
    def create_sequence(raw_seq, seq_type):
        """
        Creates a Biopython Seq object based on seq_type flag.

        Parameters:
            raw_seq  (str): raw sequence string (may contain spaces/newlines)
            seq_type (str): "DNA" or "PROTEIN"

        Returns:
            Seq: cleaned Biopython Seq object
        """
        clean_seq = "".join(raw_seq.split())  # ← now actually runs

        if seq_type == "DNA":
            allowed = set("ACGTN")
            if not all(c in allowed for c in clean_seq.upper()):
                raise ValueError("Sequence contains invalid nucleotide characters.")
            return Seq(clean_seq)

        elif seq_type == "PROTEIN":
            allowed = set("ACDEFGHIKLMNPQRSTVWY")
            if not all(c in allowed for c in clean_seq.upper()):
                raise ValueError("Sequence contains invalid amino acid characters.")
            return Seq(clean_seq)

        else:
            raise ValueError(f"Unknown seq_type '{seq_type}'. Use 'DNA' or 'PROTEIN'.")

# 1. utility class with static methods
class BioUtils:
    @staticmethod
    def transcribe_dna_to_rna(dna_seq):
        return dna_seq.transcribe()

    @staticmethod
    def translate_rna_to_protein(rna_seq):
        remainder = len(rna_seq) % 3          # must be multiple of 3 for translation
        if remainder != 0:
            rna_seq = rna_seq[:-remainder]
        return rna_seq.translate()



if __name__ == '__main__':

    #dna_storage = SequenceStorage()  # ← Singleton check: only one instance of SequenceStorage exists
    dna_storage = SequenceStorage()

    #5. coding sequence of CD28 (from NCBI) as raw string
    cd28_raw = """atgatcctcaggctgctggtgctggctctctcttctctccctcccataggctgctttgaatcctatgaagtcac
    ccaggagccatccaatgtgagcatccacttctgcactccggagctactgggctcctcaacaaagtaccctagt
    ggcccttcccacacttccccaaccatcctgagccatcggaggcctccatgaagggcaagcacttgcaggacc
    tgctttcaatacttacatgatgaatactcctcggtgaaggatcacacagggagtttatggtgctgctgagtc
    aatccaggtatacccgagggctatgatggcatatccctccatccaggaggcaaacctccggctcaaggacaa
    cttctgctcttggctctggatgtgagccagctgctccctcctcgtgctcttcttcagcctggtggctatttcc
    tcctctactggctgctgcaggctatggctctgctcttcctgctgcatctgcagcagctctgctccatgtccca
    tgccacctgttccaagttcctgcctatgtcctgcagaggattccctcctgctccagaggtaccctcaactgt
    actactctgacctgctgaagatgtcaaggatagaggccaaacccattgggcaaccctgaggcccctgtccat
    caagagattggcagagcctcacagagatgacccttggtgatgagaccctgaccccctgcagaggatctga"""

    cd28_dna = SequenceFactory.create_sequence(cd28_raw, "DNA")   # ← flag: "DNA"
    dna_storage.save("cd28_dna", cd28_dna)

    cd28_rna = BioUtils.transcribe_dna_to_rna(dna_storage.read("cd28_dna"))
    dna_storage.save("cd28_rna", cd28_rna)

    cd28_protein = BioUtils.translate_rna_to_protein(dna_storage.read("cd28_rna"))
    dna_storage.save("cd28_protein", cd28_protein)

    #5. corresponding protein sequence of CD28
    # 1>DNA to RNA 2>RNA to protein 
    print("── DNA / RNA / Protein from transcription ──")
    print(f"RNA Length   : {len(cd28_rna)} bp")
    print(f"Protein      : {dna_storage.read('cd28_protein')}")


    #protein_storage = ProteinStorage()  # ← Singleton check: only one instance of ProteinStorage exists
    protein_storage = ProteinStorage()
    
    #. insulin as a protein sequence
    insulin_raw = """MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT"""

    insulin = SequenceFactory.create_sequence(insulin_raw, "PROTEIN")  # ← flag: "PROTEIN"
    protein_storage.save("insulin", insulin)

    print("\n── Direct Protein Storage ──")
    print(f"Insulin      : {protein_storage.read('insulin')}")
    print(f"Length       : {len(protein_storage.read('insulin'))} aa")

    # ── Singleton check ───────────────────────────────────────────────────────

    print("\n── Singleton check ──")
    print(f"dna_storage is SequenceStorage() : {dna_storage is SequenceStorage()}")   # True
    print(f"protein_storage is ProteinStorage(): {protein_storage is ProteinStorage()}")  # True
    print(f"dna_storage is protein_storage   : {dna_storage is protein_storage}")     # False