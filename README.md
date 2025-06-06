﻿# M1Model_SubConversion

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

### NEURON SIMULATION RUN

The NEURON simulation for the file ran pretty smoothly and the graph was generated for the membrane potential vs time and the 2 represents 2 states of the cell.

- The resting phase [Graph](https://github.com/AceHunterr/M1Model_SubConversion/blob/master/FS3NEURONSimulationRun/FS3NEURONSimulationRun.jpeg): When the cell is resting

- The spiking phase [Graph](https://github.com/AceHunterr/M1Model_SubConversion/blob/master/FS3NEURONSimulationRun/FS3NEURONSimulationRun1.jpeg): An external input in form of an IClamp Injection is given to the cell to see the spiking behaviour.

### NeuroML Conversion for Morphologies

The cell morphologies are getting converted using the User Docs script and validated as I have attached validated files images in the folder. The main issue lies with the biophsyics conversion.

### Issue with the BioPhysics (mod files)

Let me explain via the FS3.hoc conversion only what is the issue. The BioPhysics defined for the FS3.hoc cell is defined in 9 NMODL files:

- pas – for the passive properties 
- Nafx – for the fast sodium channel 
- kdrin – for the delayed-rectifier potassium channel
- IKsin – for the slow potassium channel 
- hin – for the hyperpolarization-activated current
- kapin – for one of the A-type or persistent potassium channels
- canin – for a calcium channel mechanism
- kctin – for another potassium channel variant
- cadyn – for the calcium dynamics 

and for the NeuroML conversion workflow I need to setup the LEMS simulation file and it needs to have the mod files converted to XML something like this:

```xml
      <ionChannelMechanism id="Nafx" file="Nafx.nml.xml">
        <density value="0.045"/>
      </ionChannelMechanism>
      <ionChannelMechanism id="kdrin" file="kdrin.nml.xml">
        <density value="0.018"/>
      </ionChannelMechanism>
```

where "Nafx.nml.xml" is my converted MOD file and so on for the rest of the files.

Now what is happening is that when I am trying to convert the current MOD using the [script](https://github.com/AceHunterr/M1Model_SubConversion/blob/master/ModFileConvertor/mod2NML/src/translator.py) the MOD files present in the M1 Model are throwing errors while converting them and a manual check for the complete file would be required:

![Conversion Error Screenshot](https://raw.githubusercontent.com/AceHunterr/M1Model_SubConversion/master/ModFileConvertor/ModFileConversionError1.jpeg)

![Conversion Error Screenshot](https://raw.githubusercontent.com/AceHunterr/M1Model_SubConversion/master/ModFileConvertor/ModFileConversionError2.jpeg)

![Conversion Error Screenshot](https://raw.githubusercontent.com/AceHunterr/M1Model_SubConversion/master/ModFileConvertor/ModFileConversionError3.jpeg)


Eventually I did manage to successfully convert the kdrin.mod file into into the proper xml format. The error lied with the Procedure block defined in the mod file

I changed it from this : 

```
FUNCTION alf(v){ LOCAL va 
	
	   va=v-13
	if (fabs(va)<1e-04){
	   va=va+0.0001
		alf= (-0.018*va)/(-1+exp(-(va/25)))
	} else {
	  	alf = (-0.018*(v-13))/(-1+exp(-((v-13)/25)))
	}
}


FUNCTION bet(v) { LOCAL vb 
	
	  vb=v-23
	if (fabs(vb)<1e-04){
	  vb=vb+0.0001
		bet= (0.0054*vb)/(-1+exp(vb/12))
	} else {
	  	bet = (0.0054*(v-23))/(-1+exp((v-23)/12))
	}
}

PROCEDURE rate(v (mV)) {
    LOCAL q10, sum, aa, ab
	
	aa=alf(v) ab=bet(v) 
	
	sum = aa+ab
	inf = aa/sum
	tau = 1/(sum)
	
	
}
```

to this(Combining the alpha and beta function into one) : 

```
PROCEDURE rate(v (mV)) {
    LOCAL alpha, beta, sum, eps1, eps2
    TABLE ninf, tau DEPEND celsius FROM -100 TO 100 WITH 400
    UNITSOFF

    eps1 = (fabs(v - 13) < 1e-4) ? 1e-4 : 0
    eps2 = (fabs(v - 23) < 1e-4) ? 1e-4 : 0

    alpha = (-0.018 * ((v - 13) + eps1)) / (-1 + exp(-(((v - 13) + eps1)/25)))
    beta  = (0.0054 * ((v - 23) + eps2))  / (-1 + exp(((v - 23) + eps2)/12))

    sum = alpha + beta
    ninf = alpha / sum
    tau = 1 / sum

}

```

and then the conversion worked in the [output.nml](https://github.com/AceHunterr/M1Model_SubConversion/blob/master/ModFileConvertor/mod2NML/src/output.nml).

But the manual identification, correction and conversion for each file would require some time and hence the NeuroML workflow simulation for the single cell(in our case FS3.hoc) won't be possible since the LEMS requires so.

### Running the complete NEURON Model

Since the current model is a very big and it has various several parameters and networks running it locally was not supported so I tried a workaround along with the “Web based GUI setup via OpenSourceBrain” to get a look at the logs during the execution of the model. I used the kaggle’s online platform by creating a Notebook for running the model: 

[https://www.kaggle.com/code/mehul26z/m1neuron-first-compiled-nb](https://www.kaggle.com/code/mehul26z/m1neuron-first-compiled-nb)


### Conclusion

Apart from the MOD files conversion hiccup rest I followed all the steps in the conversion to NeuroML guide and have uploaded my proof of work so far in this repository.
