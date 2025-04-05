import pickle
from netpyne import specs, sim
from netpyne.export import exportNeuroML
import os
# -------------------------------
# 1. Load cell parameters from pkl file
# -------------------------------
pkl_filename = "./cells/IT_full_BS1578_cellParams.pkl"
with open(pkl_filename, "rb") as f:
    cellParams = pickle.load(f)

# -------------------------------
# 2. Create a NetParams object and add the cell parameters
# -------------------------------
netParams = specs.NetParams()
# Assign the loaded cell parameters a label; here we use "IT_cell"
netParams.cellParams["IT_cell"] = cellParams

# (Optionally, you can set a condition to identify this cell type)
netParams.cellParams["IT_cell"]["conds"] = {"cellType": "IT_cell"}

# -------------------------------
# 3. Export the cell (or network) to NeuroML
# -------------------------------
# We use the built-in export function.
# The function convertNetParams2NeuroML() will create a NeuroML file from the netParams object.
# (You can also include a SimConfig if you wish to export a complete network instance.)
nml_filename = "IT_cell_converted.nml"
# Export the NetParams (which here only contains our cell) to a NeuroML file
exportNeuroML.convertNetParams2NeuroML(netParams, filename=nml_filename)
print("NeuroML file generated:", os.path.abspath(nml_filename))

# -------------------------------
# 4. Verify the conversion by reading the NeuroML file
# -------------------------------
# We use the neuroml Python package (pyNeuroML) to load the NeuroML document.
try:
    from neuroml import loaders
except ImportError:
    print("pyNeuroML not installed. You can install it via pip: pip install neuroml")
    exit()

# Load the NeuroML document
nml_doc = loaders.read_neuroml2_file(nml_filename)
print("NeuroML document ID:", nml_doc.id)
# List the cells defined in the NeuroML document
if hasattr(nml_doc, 'cells'):
    print("Cells in the NeuroML file:")
    for cell in nml_doc.cells:
        print(" - Cell ID:", cell.id)
else:
    print("No cells were found in the NeuroML file. Please verify the export.")
