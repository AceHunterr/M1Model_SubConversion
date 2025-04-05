import os
import matplotlib.pyplot as plt
from pyneuroml import pynml

# Define the NeuroML file and simulation ID
nml_file = "FS3_cell.nml"
sim_id = "FS3_sim"
duration = 100    
dt = 0.025        

pynml.run_lems_with_jneuroml(os.path.abspath(nml_file), 
                             max_memory="2G",
                             nogui=True,
                            #  duration=duration,
                            #  dt=dt,
                            #  sim_id=sim_id
                             )

# Assuming the simulation output is saved in a file named something like 'FS3_sim_voltage.dat'
output_file = f"{sim_id}_voltage.dat"

# Load and plot the voltage trace 
times = []
voltages = []
with open(output_file, 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            times.append(float(parts[0]))
            voltages.append(float(parts[1]))

plt.figure(figsize=(8, 4))
plt.plot(times, voltages, label="Soma Voltage")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Voltage (mV)")
plt.title("FS3 Cell Simulation in NeuroML")
plt.legend()
plt.show()
