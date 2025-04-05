# from neuron import h, gui
# import matplotlib.pyplot as plt

# # -------------------------------------------------------------------------
# # Load the FS3 cell morphology file (FS3.hoc)
# # -------------------------------------------------------------------------
# # Make sure the FS3.hoc file is in the same directory or update the path accordingly.
# h.load_file("./cells/FS3.hoc")

# # -------------------------------------------------------------------------
# # Instantiate the FS cell (PV_simple cell)
# # -------------------------------------------------------------------------
# # The FS3.hoc file defines a template 'FScell'. Here we create an instance.
# fs_cell = h.FScell()  

# # Alternatively, if the hoc file already instantiates a cell as 'FScell1',
# # you can use:
# # fs_cell = h.FScell1

# # -------------------------------------------------------------------------
# # Set up recording vectors for time and the soma voltage.
# # -------------------------------------------------------------------------
# t_vec = h.Vector().record(h._ref_t)
# v_vec = h.Vector().record(fs_cell.soma(0.5)._ref_v)

# # -------------------------------------------------------------------------
# # Initialize simulation parameters
# # -------------------------------------------------------------------------
# # The FS3.hoc file initializes the cell with a resting potential of -73 mV.
# h.finitialize(-73)
# # Run the simulation for 100 ms (adjust as desired)
# h.continuerun(100)

# # -------------------------------------------------------------------------
# # Plot the recorded voltage trace
# # -------------------------------------------------------------------------
# plt.figure(figsize=(8, 4))
# plt.plot(t_vec, v_vec, label="Soma Voltage")
# plt.xlabel("Time (ms)")
# plt.ylabel("Membrane Voltage (mV)")
# plt.title("FS3 (PV_simple) Cell Simulation")
# plt.legend()
# plt.show()




from neuron import h, gui
import matplotlib.pyplot as plt

# Load the FS3.hoc file
h.load_file("./cells/FS3.hoc")

# Instantiate the FS3 cell
fs_cell = h.FScell()

# ---------------------------
# Add a current clamp
# ---------------------------
stim = h.IClamp(fs_cell.soma(0.5))
stim.delay = 5   # start injection at 5 ms
stim.dur = 40    # last for 40 ms
stim.amp = 0.2   # inject 0.2 nA

# Record time and voltage
t_vec = h.Vector().record(h._ref_t)
v_vec = h.Vector().record(fs_cell.soma(0.5)._ref_v)

# Initialize and run
h.finitialize(-73)
h.continuerun(100)

# Plot results
plt.figure(figsize=(8, 4))
plt.plot(t_vec, v_vec, label="Soma Voltage")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Voltage (mV)")
plt.title("FS3 Cell with Current Injection")
plt.legend()
plt.show()


