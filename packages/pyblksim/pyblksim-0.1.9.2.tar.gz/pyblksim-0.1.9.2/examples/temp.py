from pyblksim.common.sources import Clock, DC, UartTx
from pyblksim.common.sinks import Scope, Spectrum
from pyblksim.common.math import Squaring, GEQ, Product
from pyblksim.common.filters import LPF_FIR, BPF_FIR
from pyblksim.sims.basics import Environment

# Initialize the simulation environment
env = Environment.init()

### Simulation settings
simulation_time = 2e-3  # Total simulation time in seconds
sampling_rate = 10e6  # Sampling frequency in Hz

# Sources
clock_signal = Clock(env, frequency=1e6, sampling_frequency=sampling_rate)
uart_transmitter = UartTx(env, sampling_frequency=sampling_rate, data_byte=0xAA, baud_rate=100e3)
dc_offset = DC(env, amplitude=0.1, sampling_frequency=sampling_rate)


uart_scope = Scope(env, sampling_frequency=sampling_rate, name="UART Output")
uart_spectrum = Spectrum(env, sampling_frequency=sampling_rate, name="UART Spectrum")

uart_scope.input = uart_transmitter.output
uart_spectrum.input = uart_transmitter.output


# Run the simulation
env.run(until=simulation_time)


uart_scope.plot()
uart_spectrum.plot()