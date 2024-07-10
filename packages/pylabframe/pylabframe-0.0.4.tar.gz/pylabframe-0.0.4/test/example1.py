import numpy as np
import matplotlib.pyplot as plt
import time

# load pylabframe
import pylabframe as lab
import pylabframe.data, pylabframe.data.fitters
from pylabframe.hw import device, drivers
from pylabframe.hw.drivers.keysightvisa import KeysightESA
from pylabframe.hw.drivers.santecvisa import TSL

# connect to devices
laser: TSL = device.get_device('tsl_on_com10')
esa: KeysightESA = device.get_device('esa')

# set up experiment
laser.wavelength = 1550e-9
esa.span = 20e3
esa.center_frequency = 1.3e6
esa.rbw = 1.

# acquire & save
spectrum = esa.acquire_trace()  # ESA metadata is auto-added
spectrum.metadata['laser_wavelength'] = laser.wavelength
#     timestamp is auto-added
spectrum.save_npz(lab.path.save_path("mech_spectrum.npz"))

# fit, initial guess is automatic
spectrum_fit = spectrum.fit(lab.data.fitters.Lorentzian)
spectrum_fit.summary()  # print summary of fit params

# plot
fig, ax = plt.subplots()
spectrum.plot(plot_axis=ax)
spectrum_fit.plot(plot_axis=ax)


### example 2: for loop
wavelengths = np.linspace(1540e-9, 1560e-9, 21)

sweep_dir = lab.path.TimestampedDir('optical_spring_msmt')
spectra = []
for i, wl in enumerate(wavelengths):
    laser.wavelength = wl
    time.sleep(0.2)

    spectrum = esa.acquire_trace()
    spectrum.metadata['laser_wavelength'] = laser.wavelength
    spectrum.save_npz(sweep_dir.file(f"sweep_pt{i}.npz"))
    spectra.append(spectrum)

# combine spectra into 2d data array & plot
spectrogram = lab.data.NumericalData.stack(spectra, wavelengths)
fig, axes = plt.subplots(1,2)
spectrogram.plot(plot_axis=axes[0])

# fit spectra & plot centre frequencies
spectrum_fits = [s.fit(lab.data.fitters.Lorentzian) for s in spectra]
fitted_freqs = [f['center'] for f in spectrum_fits]
fitted_freqs = lab.data.NumericalData(wavelengths, fitted_frequencies)
fitted_freqs.plot(plot_axis=axes[1])
