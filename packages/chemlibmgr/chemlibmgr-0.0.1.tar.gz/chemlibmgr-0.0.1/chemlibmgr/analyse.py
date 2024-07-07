from collections import Counter
import os
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.SaltRemover import SaltRemover

from chemlibmgr import config, io


def molecule_properties(mol, classify=False):
    properties = {}
    descriptors_to_calculate = [
        ('Molecular_Weight', rdMolDescriptors.CalcExactMolWt),
        ('HBD', rdMolDescriptors.CalcNumHBD),
        ('HBA', rdMolDescriptors.CalcNumHBA),
        ('Rotatable_Bonds', rdMolDescriptors.CalcNumRotatableBonds),
        ('Rings', rdMolDescriptors.CalcNumRings),
        ('Stereo_Centers', rdMolDescriptors.CalcNumAtomStereoCenters),
        ('sp3_Carbons_Fraction', rdMolDescriptors.CalcFractionCSP3),
        ('Heavy_Atoms', Descriptors.HeavyAtomCount),
        ('N_O_Atoms', rdMolDescriptors.CalcNumLipinskiHBA),
        ('LogP', Descriptors.MolLogP),
        ('TPSA', rdMolDescriptors.CalcTPSA)
    ]

    for prop, descriptor in descriptors_to_calculate:
        try:
            properties[prop] = descriptor(mol)
        except Exception as e:
            print("An error occurred:", e)
            properties[prop] = -1000

    if classify:
        properties['Classification'] = classify_molecule(properties)

    return properties


def classify_molecule(properties):
    if (
        properties['LogP'] <= 3 and
        properties['Molecular_Weight'] > 110 and
        properties['TPSA'] <= 110 and
        properties['HBD'] <= 3 and
        properties['HBA'] <= 5 and
        properties['Rotatable_Bonds'] <= 3 and
        properties['Rings'] <= 1 and
        properties['Heavy_Atoms'] <= 18
    ):
        return 'Fragment'
    elif (
        0 <= properties['LogP'] <= 3 and
        250 <= properties['Molecular_Weight'] <= 375 and
        properties['TPSA'] < 110 and
        properties['HBD'] <= 2 and
        properties['HBA'] <= 5 and
        properties['Rotatable_Bonds'] <= 10 and
        properties['Stereo_Centers'] <= 1
    ):
        return 'Leadlike'
    elif (
        -1 <= properties['LogP'] <= 4 and
        250 <= properties['Molecular_Weight'] <= 500 and
        50 < properties['TPSA'] < 130 and
        properties['HBD'] <= 5 and
        properties['HBA'] <= 10 and
        properties['Rotatable_Bonds'] <= 10 and
        properties['Stereo_Centers'] <= 3
    ):
        return 'Druglike'
    elif (
        -1.5 <= properties['LogP'] <= 5.5 and
        150 <= properties['Molecular_Weight'] <= 575 and
        30 < properties['TPSA'] < 150 and
        properties['HBD'] <= 5 and
        properties['HBA'] <= 12 and
        properties['Rotatable_Bonds'] <= 10 and
        properties['Stereo_Centers'] <= 3
    ):
        return 'Near-Druglike'
    else:
        return 'Undetermined'


def gen_libfile_report(file_path, file_format=None, output_dir=None,
                       gen_csv=False, gen_report=False):
    if not gen_csv and not gen_report:
        return

    salts = os.path.join(config.CLMDIR, 'data', 'salts')

    uncharger = rdMolStandardize.Uncharger()
    remover = SaltRemover(defnFilename=salts)
    results = []

    mols = io.load(file_path, file_format)
    for mol in mols:
        if mol is not None:
            mol = uncharger.uncharge(mol)
            mol = remover.StripMol(mol)
            Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
            props = molecule_properties(mol, classify=True)
            props['Name'] = mol.GetProp('_Name')
            results.append(props)

    df_props = pd.DataFrame(results)

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(file_path))

    if gen_csv:
        output_path = os.path.join(output_dir, 'props.csv')
        df_props.to_csv(output_path, index=False)

    if gen_report:
        output_path = os.path.join(output_dir, 'report.pdf')
        plot_props_charts(df_props, output_path)


def plot_props_charts(data_input, output_path):
    if isinstance(data_input, str):
        df = pd.read_csv(data_input)
    elif isinstance(data_input, pd.DataFrame):
        df = data_input
    else:
        raise ValueError("Input must be CSV file path or pandas DataFrame.")

    def plot_bar(ax, data, bins, title, gap=False, fontsize=5):
        bin_counts = Counter(data)
        all_bin_counts = {bin: bin_counts.get(bin, 0) for bin in bins}
        total_count = sum(all_bin_counts.values())
        bin_percentages = [count / total_count if total_count >
                           0 else 0 for count in all_bin_counts.values()]
        if gap:
            ax.bar(bins, bin_percentages)
        else:
            ax.bar(bins, bin_percentages, width=1, edgecolor='black')
        ax.set_xticks(bins)
        ax.yaxis.set_major_formatter(
            ticker.PercentFormatter(xmax=1, decimals=1))
        ax.tick_params(axis='both', which='major', labelsize=fontsize)
        ax.set_title(title, fontsize=fontsize+4)

    def plot_hist(ax, data, bins, title, fontsize=5):
        weights = np.ones_like(data) / len(data)
        ax.hist(data, bins=bins, weights=weights, edgecolor='black')
        ax.set_xticks(bins)
        ax.yaxis.set_major_formatter(
            ticker.PercentFormatter(xmax=1, decimals=1))
        ax.tick_params(axis='both', which='major', labelsize=fontsize)
        ax.set_title(title, fontsize=fontsize+4)

    fig, axs = plt.subplots(nrows=6, ncols=2, figsize=(8.268, 11.693))

    categories = ['Druglike', 'Leadlike',
                  'Near-Druglike', 'Fragment', 'Undetermined']
    plot_bar(axs[0][0], df['Classification'], categories,
             'Classification', gap=True)

    plot_hist(axs[0][1], df['Molecular_Weight'], range(0, 840, 40),
              'Molecular Weight')

    plot_bar(axs[1][0], df['HBD'], range(0, 16),
             'Number of hydrogen bond donors')

    plot_bar(axs[1][1], df['HBA'], range(0, 16),
             'Number of hydrogen bond acceptors')

    plot_bar(axs[2][0], df['Rotatable_Bonds'], range(0, 21),
             'Number of rotatable bonds')

    plot_bar(axs[2][1], df['Rings'], range(0, 16),
             'Number of rings')

    plot_bar(axs[3][0], df['Stereo_Centers'], range(0, 11),
             'Number of stereogenic centers')

    plot_hist(axs[3][1], df['sp3_Carbons_Fraction'], np.arange(0.0, 1.1, 0.1),
              'Fraction of sp3 carbons')

    plot_bar(axs[4][0], df['Heavy_Atoms'], range(4, 46),
             'Number of heavy atoms')

    plot_bar(axs[4][1], df['N_O_Atoms'], range(0, 21),
             'Sum of nitrogen and oxygen atoms')

    plot_hist(axs[5][0], df['LogP'], np.arange(-3, 8.5, 0.5),
              'Logarithm of the atomistic partition coefficient')

    plot_hist(axs[5][1], df['TPSA'], range(0, 260, 10),
              'Fragment-based topological polar surface area')

    plt.tight_layout()
    plt.savefig(output_path)
