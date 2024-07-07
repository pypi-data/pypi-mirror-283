# chemlibmgr

## Introduction

`chemlibmgr` is a Python library designed to simplify the management of chemical compound libraries databases.

## Features

- **Data Handling**: Easily manage compound properties such as molecular weight, melting point, and more.
- **Library Analysis**: Easily analyze the property distribution of compounds in your library.
- **Search Functionality**: Perform quick searches based on compound properties or chemical structures.

## Installation

To install `chemlibmgr`, use pip:

```bash
pip install chemlibmgr
```

## Usage

### Basic Usage

```python
from chemlibmgr.manager import Manager

# Initialize the manager with your database configuration
mgr = Manager(database="compounds.db")

# Add new compounds from smiles file
mgr.add_compound('/path/to/smifile', calc_props=False)

# Retrieve compounds
compounds = mgr.search_compounds({'name': 'Aspirin'})
for compound in compounds:
    print(compound)

# Add a new property field
mgr.add_field('Classification', 'TEXT')

# Update a compound's property
mgr.update_compound_property(
    smiles='CC(=O)Oc1ccccc1C(=O)O', Classification='Drug')

# Delete a compound
mgr.delete_compound(name='Aspirin')

mgr.close()
```

## Contributing

We welcome contributions to improve `chemlibmgr`. If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

## License

This project is licensed under the Apache License - see the [Apache 2.0 license](https://github.com/ojtian/chemlibmgr/blob/main/LICENSE) file for details.
