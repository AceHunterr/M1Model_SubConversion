from neuron import h
import pytest

def test_model_load():
    """Test if the HOC model loads successfully."""
    h.load_file("./cells/PTcell.hoc")
    assert len(h.allsec()) > 0, "No sections found in the model!"

def test_sections_exist():
    """Check if the required neuron sections exist."""
    h.load_file("./cells/PTcell.hoc")
    sections = [sec.name() for sec in h.allsec()]
    required_sections = ["soma", "axon", "dend"]
    for sec in required_sections:
        assert any(sec in s for s in sections), f"Missing {sec} section!"

def test_action_potential():
    """Ensure the neuron fires an action potential when stimulated."""
    h.load_file("./cells/PTcell.hoc")

    # Create a current clamp
    stim = h.IClamp(h.soma(0.5))
    stim.delay = 5  # Stimulate after 5ms
    stim.dur = 5    # Duration of 5ms
    stim.amp = 0.5  # Amplitude of 0.5 nA

    # Record membrane potential
    v = h.Vector().record(h.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    # Run the simulation
    h.tstop = 40
    h.finitialize(-65)
    h.run()

    # Check if voltage crosses 0 mV (spike)
    assert max(v) > 0, "No action potential detected!"

def test_synaptic_response():
    """Check if a synapse generates an EPSP."""
    h.load_file("./cells/PTcell.hoc")

    # Create a synapse and stimulate it
    syn = h.ExpSyn(h.soma(0.5))
    syn.tau = 5  # Synaptic time constant

    stim = h.NetStim()
    stim.number = 1
    stim.start = 10  # Start at 10 ms

    nc = h.NetCon(stim, syn)
    nc.weight[0] = 0.1  # Synaptic weight

    v = h.Vector().record(h.soma(0.5)._ref_v)
    h.tstop = 40
    h.finitialize(-65)
    h.run()

    assert max(v) > -50, "No synaptic response detected!"

if __name__ == "__main__":
    import pytest
    pytest.main()