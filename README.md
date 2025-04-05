# M1Model_SubConversion

## Overview
This repository contains the conversion and the research so far for the M1 model from NEURON to NeuroML. I have tried converting and running the simulations for the Fast Spiking FS3 cell and have attached data and images folder wise.

**Note** : I have used the separated the files and each step that I broke down the conversion in separate folder therefore the "PATHs" may be ambigous in the script  but would be correct in main conversion.

## Repository Structure

- **sim**  
    The original NEURON model code for the M1Model from the [SunnyDownstate](https://github.com/suny-downstate-medical-center/M1_NetPyNE_CellReports_2023) Repository.

- **FS3NEURONSimulationRun**  
    Contains the script and the image results for NEURON Simulation run for FS3

- **FS3NeuroMLConversion**  
  Houses conversion tools and scripts that transform the NEURON model into NeuroML format.

  I have essentially used the script from the [UserDocs](https://docs.neuroml.org/Userdocs/SingleNeuronExample.html)

  But as present in the script only the morphology is generated in NeuroML since the attribute "includeBiophysicalProperties" is False.

    ```py
        export_to_neuroml2(
            loader_hoc_file,
            output_nml_file,
            includeBiophysicalProperties=True,# Exclude biophysical properties
            validate=False,  
             execution
        )
    ```

    Converted and validated 2 Cell morphologies FS3.hoc and LTS3.hoc .

- **FS3NeuroMLSimulationRun**  
  Wrote a script for a single cell simulation using the LEMS file generated.

- **ModFileConvertor**  
  Dedicated to converting NEURON mod (BioPhysics of the cell) files into a format compatible with NeuroML.

  The script that is used for translation is from the github [mod2nml](https://github.com/ninadakolekar/mod2nml)

- **MiscllenousFiles**  
  Some extra files and the OMT test files written.

## Workflow and Issue Facing

For converting and running simulation for a subpart of the complete model I was following the workflow as I mentioned in my proposal and worked on the FS3 cell.



