import bdsim

# Create a BDSim instance
sim = bdsim.BDSim()

# Create a block diagram
bd = sim.blockdiagram()

# Define parameters common to all waveforms
TSIM = 5  # in seconds
FS = 1000  # in Hz

# Create a square wave source
square_wave = bd.WAVEFORM(wave='square', freq=1, amplitude=5, offset=0, duty=0.5)

# Create a sine wave source
sine_wave = bd.WAVEFORM(wave='sine', freq=1, amplitude=5, offset=0)

# Create a ramp wave source - Assuming it starts at 0, goes to 5 over 5 seconds
ramp_wave = bd.RAMP(0, off=0, slope=1) #, duration=TSIM)

# Create scopes for each waveform
square_scope = bd.SCOPE()
sine_scope = bd.SCOPE()
ramp_scope = bd.SCOPE()  # Scope for ramp wave

# Connect each source to its respective scope
bd.connect(square_wave, square_scope)
bd.connect(sine_wave, sine_scope)
bd.connect(ramp_wave, ramp_scope)  # Connect ramp wave to its scope

# Compile the block diagram
bd.compile()

# Run the simulation
results = sim.run(bd, T=TSIM, dt=1/FS, block=False)
