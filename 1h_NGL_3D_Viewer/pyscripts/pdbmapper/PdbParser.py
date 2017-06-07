'''
   pdbparser.py - Yevheniy Chuba - 6/1/2017
   Parse local or external (PDB Database) 3D structure files (.pdb, .cif)

   Usage:
    parser = PdbParser("2128-1.pdb").pdb_processing()
    output: [['L', 'DIQ...'], ['H', 'EVQL...']]
'''
import os
from Bio.PDB import *
from Bio.Seq import Seq

class PdbParser:
    '''
        PdbParser extracts amino acid sequence from PDB structure,
        either downloaded from PDB database or uploaded localy .pdb file

        Args:
            pdb_struct_name (string): name of the file or PDB database ID
            external (bool): True indicates the structure comes from an external
                             PDB database; default is False (local .pdb file)
        Returns:
            Extracted amino acid sequence from the PDB file, including chain information
    '''

    def __init__(self, struct_name, struct_dir='PDB_Struct', external=False):
        self.struct_name = struct_name
        self.struct_dir = struct_dir
        self.external = external

    def pdb_processing(self):
        """
            Process either uploaded or externally downloaded 3D structure
        """
        if self.external:
            self.pdb_struct = self.get_external_struct()
        else:
            self.pdb_struct = self.get_uploaded_struct()

        extracted_seq = self.extract_seq_from_structure(self.pdb_struct)
        return extracted_seq

    def get_external_struct(self):
        """
            Create Structure object from externally downloed (PDB Database) structure file (.cif)
        """
        self.download_structure()
        parser = MMCIFParser()
        structure = parser.get_structure('STRUCT_OBJ',
                                         os.path.join(self.struct_dir, self.struct_name) + '.cif')
        return structure

    def get_uploaded_struct(self):
        """
            Create Structure object from locally uploaded structure file (.pdb)
        """
        parser = PDBParser()
        structure = parser.get_structure('STRUCT_OBJ',
                                         os.path.join(self.struct_dir, self.struct_name))
        return structure

    def download_structure(self):
        """
            Download structure from PDB database based on PDB ID
        """
        pdbl = PDBList()
        pdbl.retrieve_pdb_file(self.struct_name, pdir=self.struct_dir)

    def extract_seq_from_structure(self, struct):
        """
            Extract Polypeptides from a Structure Object
        """
        ppb = PPBuilder() # Polypeptide builder object
        aa_seqs = []
        chains = struct.get_chains()
        for pp in ppb.build_peptides(struct):
            seq = pp.get_sequence()
            aa_seqs.append(str(seq))
        chain_aa_map = [[chain.id, aa_seqs[index]] for index, chain in enumerate(chains)]
        return chain_aa_map
