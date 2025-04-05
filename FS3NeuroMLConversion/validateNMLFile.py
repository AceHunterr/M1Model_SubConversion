from neuroml import NeuroMLDocument
from neuroml.utils import validate_neuroml2

# Load the NeuroML file
# nml_doc = NeuroMLDocument(id="FS3_cell", load_from_file="FS3_cell.nml")
nml_doc = NeuroMLDocument(id="LTS3_cell", load_from_file="LTS3_cell.nml")

# Validate the file
validate_neuroml2("LTS3_cell.nml")