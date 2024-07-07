from rdkit import Chem

from chemlibmgr import analyse, db, io


class Manager:
    def __init__(self, database: str):
        self.db = db.MolDB(database)

    def add_field(self, field_name: str, field_type: str):
        self.db.add_field(field_name, field_type)

    def add_compound(self, compound_input, calc_props: bool = True, **kwargs):
        if isinstance(compound_input, str):  # File path
            mols = io.load(compound_input)
        elif isinstance(compound_input, Chem.Mol):  # RDKit Mol object list
            mols = compound_input
        else:
            raise ValueError("Unsupported input type.")

        if calc_props:
            self.db.add_field('Molecular_Weight', 'REAL')
            self.db.add_field('HBD', 'INTEGER')
            self.db.add_field('HBA', 'INTEGER')
            self.db.add_field('Rotatable_Bonds', 'INTEGER')
            self.db.add_field('Rings', 'INTEGER')
            self.db.add_field('Stereo_Centers', 'INTEGER')
            self.db.add_field('sp3_Carbons_Fraction', 'REAL')
            self.db.add_field('Heavy_Atoms', 'INTEGER')
            self.db.add_field('N_O_Atoms', 'INTEGER')
            self.db.add_field('LogP', 'REAL')
            self.db.add_field('TPSA', 'REAL')
            self.db.add_field('Classification', 'TEXT')
            for mol in mols:
                if mol is not None:
                    name = mol.GetProp('_Name')
                    smiles = Chem.MolToSmiles(mol)
                    properties = analyse.molecule_properties(
                        mol, classify=True)
                    self.db.add_compound(name, smiles, **properties)
        else:
            for mol in mols:
                if mol is not None:
                    name = mol.GetProp('_Name')
                    smiles = Chem.MolToSmiles(mol)
                    self.db.add_compound(name, smiles)

    def delete_compound(self, **kwargs):
        return self.db.delete_compound(**kwargs)

    def update_compound_property(self, name: str = None, smiles: str = None, compound_id: int = None, **kwargs):
        self.db.update_compound_property(name, smiles, compound_id, **kwargs)

    def search_compounds(self, query: dict):
        return self.db.search_compounds(query)

    def get_all_compounds(self):
        return self.db.search_compounds({})

    def close(self):
        self.db.close()
