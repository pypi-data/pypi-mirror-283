from pyblksim.common.sources import SquareWave, SineWave, BandLimitedWhiteNoise, Ramp
from pyblksim.common.sinks import Scope, Spectrum
from pyblksim.sims.basics import Environment

# User settings
TSIM = 5  # Simulation time in seconds
FS = 1000   # Sampling frequency in Hz

# Create simulation environment
env = Environment.init()

# Create a square wave source
square_wave = SquareWave(env, offset=0, amplitude=5, sampling_frequency=FS, duty_cycle=0.5)

# Create a sine wave source
sine_wave = SineWave(env, amplitude=5, frequency=5, sampling_frequency=FS)

# Create a BandLimitedWhiteNoise source
band_limited_white_noise = BandLimitedWhiteNoise(env, amplitude=5, sampling_frequency=FS)

# Create a Ramp source
ramp_signal = Ramp(env, start=0, slope=1, sampling_frequency=FS)  # Adjust 'start' and 'slope' as needed

# Create scopes to observe the waves
square_scope = Scope(env, sampling_frequency=FS, name="Square Wave Scope")
sine_scope = Scope(env, sampling_frequency=FS, name="Sine Wave Scope")
noise_scope = Scope(env, sampling_frequency=FS, name="Noise Scope")
ramp_scope = Scope(env, sampling_frequency=FS, name="Ramp Scope")

# Create spectrum analyzers for each signal
square_spectrum = Spectrum(env, sampling_frequency=FS, name="Square Wave Spectrum")
sine_spectrum = Spectrum(env, sampling_frequency=FS, name="Sine Wave Spectrum")
noise_spectrum = Spectrum(env, sampling_frequency=FS, name="Noise Spectrum")
ramp_spectrum = Spectrum(env, sampling_frequency=FS, name="Ramp Spectrum")

# Connect sources to scopes 
square_scope.input = square_wave.output
sine_scope.input = sine_wave.output
noise_scope.input = band_limited_white_noise.output
ramp_scope.input = ramp_signal.output


# Run the simulation
env.run(until=TSIM)

# Plot the results
square_scope.plot()
sine_scope.plot()
noise_scope.plot()
ramp_scope.plot()
