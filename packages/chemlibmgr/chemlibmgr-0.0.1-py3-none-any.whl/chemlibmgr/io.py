import csv
import os
from rdkit import Chem


def load(file_path, file_format=None):
    if file_format is None:
        file_format = os.path.splitext(file_path)[1].lower()[1:]
    if file_format == 'sdf':
        return Chem.SDMolSupplier(file_path)
    elif file_format == 'smi':
        return load_smi(file_path)
    elif file_format == 'mol':
        return [Chem.MolFromMolFile(file_path)]
    elif file_format == 'pdb':
        return Chem.PDB.MolSupplier(file_path)
    elif file_format == 'mol2':
        return Chem.MolFromMol2File(file_path)
    elif file_format == 'cml':
        return Chem.CML.MolSupplier(file_path)
    elif file_format == 'mae':
        return Chem.MaeMolSupplier(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")


def save(mols, file_path, file_format=None):
    if file_format is None:
        file_format = os.path.splitext(file_path)[1].lower()[1:]

    if file_format == 'sdf':
        writer = Chem.SDWriter(file_path)
    elif file_format == 'smi':
        writer = Chem.SmilesWriter(file_path)
    elif file_format == 'mae':
        writer = Chem.MaeWriter(file_path)
    elif file_format == 'mol':
        if len(mols) != 1:
            raise ValueError("MOL format only supports single molecule.")
        Chem.MolToMolFile(mols[0], file_path)
        return
    elif file_format == 'pdb':
        writer = Chem.PDBWriter(file_path)
    elif file_format == 'mol2':
        with open(file_path, 'w') as f:
            for mol in mols:
                f.write(Chem.MolToMol2Block(mol))
                f.write('\n')
    elif file_format == 'cml':
        writer = Chem.CML.MolWriter(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")

    for mol in mols:
        if mol is not None:
            writer.write(mol)
    if hasattr(writer, 'close'):
        writer.close()


def load_smi(file_path):
    mols = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            if len(row) >= 2:
                smi = row[0]
                name = ' '.join(row[1:])
                mol = Chem.MolFromSmiles(smi)
                if mol is not None:
                    mol.SetProp("_Name", name)
                    mols.append(mol)
    return mols


def convert(input_file, output_file, input_format=None, output_format=None):
    mols = load(input_file, input_format)
    save(mols, output_file, output_format)
