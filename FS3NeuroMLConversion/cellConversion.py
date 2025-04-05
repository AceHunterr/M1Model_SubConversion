# from neuron import h
# h.load_file("./cells/FS3.hoc")


#!/usr/bin/env python3
"""
Convert cell morphology to NeuroML.

This script exports the morphology of a NEURON cell defined in a .hoc file
to a NeuroML file using pyNeuroML.

Usage: python cellConversion.py
"""


import os
from pyneuroml.neuron import export_to_neuroml2
from neuron import h


def main():
    """
    Convert a NEURON .hoc file to a NeuroML file.

    :returns: None
    """
    # Set the path to the compiled mechanisms
    os.environ["NRNMECH_LIB_PATH"] = "../sim/x86_64"

    # Define the input .hoc file and output NeuroML file
    # hoc_file = "./cells/FS3.hoc"
    hoc_file = "./cells/LTS3.hoc"
    # output_nml_file = "FS3_cell.nml"
    output_nml_file = "LTS3_cell.nml"

    # Create a temporary loader .hoc file
    loader_hoc_file = "temp_loader.hoc"
    loader_hoc_content = f"""
    load_file("stdrun.hoc")
    xopen("{hoc_file}")
    objref cell
    cell = new LTScell()  
    """

    # Write the loader .hoc file
    with open(loader_hoc_file, "w") as f:
        f.write(loader_hoc_content)

    # Export the morphology to NeuroML
    export_to_neuroml2(
        loader_hoc_file,
        output_nml_file,
        includeBiophysicalProperties=True,  # Exclude biophysical properties
        validate=False,  # Skip validation for faster execution
    )

    # Clean up the temporary loader .hoc file
    os.remove(loader_hoc_file)

    print(f"Conversion complete! NeuroML file saved as {output_nml_file}")


if __name__ == "__main__":
    main()