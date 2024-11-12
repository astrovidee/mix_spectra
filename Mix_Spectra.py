# import libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams['font.family'] = 'Georgia'  # Change 'serif' to your desired font

# Read land spectrum (three columns: wavelength, reflectance, error)
lamda, spectrum_a = [], []
with open('Land_Shields2013.txt', 'r') as f:
    for line in f:
        split_line = line.split()
        lamda.append(float(split_line[0]))
        spectrum_a.append(float(split_line[1]))

# Read biota spectrum (wavelength in microns, reflectance, and error)
wave, spectrum_b = [], []
with open('BVdry_calibrated.txt', 'r') as f:
    for line in f:
        split_line = line.split()
        wave.append(float(split_line[0]) * 10**-3)  # Convert wavelength to microns
        spectrum_b.append(float(split_line[1]))
        
with open('Ligia_Land.txt', 'r') as f:
    line = f.readlines()
    lamda_ligia= [float(line.split()[0]) for line in line]
    flux_ligia= [float(line.split()[1]) for line in line] 
    lamda_ligia = [x * 10**-3 for x in lamda_ligia]
    
# Convert lists to numpy arrays
lamda = np.array(lamda)
spectrum_a = np.array(spectrum_a)
wave = np.array(wave)
spectrum_b = np.array(spectrum_b)

# Interpolation: Create a common wavelength grid
if not np.array_equal(lamda, wave):
    # Ensure the wavelength ranges overlap
    min_common_wavelength = max(lamda[0], wave[0])
    max_common_wavelength = min(lamda[-1], wave[-1])

    if min_common_wavelength >= max_common_wavelength:
        raise ValueError("The wavelength ranges of land and biota do not overlap.")

    # Create a common wavelength grid
    common_wavelengths = np.linspace(min_common_wavelength, max_common_wavelength, num=len(lamda))

    # Interpolate both spectra to the common wavelength grid
    interp_land = interp1d(lamda, spectrum_a, kind='linear', fill_value="extrapolate")
    interp_biota = interp1d(wave, spectrum_b, kind='linear', fill_value="extrapolate")

    spectra_land_resampled = interp_land(common_wavelengths)
    spectra_biota_resampled = interp_biota(common_wavelengths)
else:
    # If the wavelengths match, no need to resample
    common_wavelengths = lamda
    spectra_land_resampled = spectrum_a
    spectra_biota_resampled = spectrum_b

# Mixing ratio for interpolation
mixing_ratio = 0.50

# Interpolating the mixed spectrum
mixed_spectrum = (1 - mixing_ratio) * spectra_land_resampled + mixing_ratio * spectra_biota_resampled
#file_name = f"Mix_{1-mixing_ratio}land_{mixing_ratio}biota.txt"

#Combine arrays
combined_array = np.column_stack((common_wavelengths, mixed_spectrum) )
# Save the array using np.savetxt()
np.savetxt('test_mix_land.txt', combined_array)


# Plotting the original and mixed spectra
plt.figure(figsize=(8, 6))
plt.ylim(0,1)
plt.xlim(0,2.5)
#plt.plot(lamda, spectrum_a, label='Ocean Spectrum')
#plt.plot(wave, spectrum_b, label='Biota Spectrum')
plt.plot(common_wavelengths, mixed_spectrum, label='Vidya Snowball', linestyle='--')
#plt.plot(lamda_ligia, flux_ligia, label = 'Ligia Snowball')
plt.plot()
# Add labels and legends
plt.xlabel('Wavelength (microns)', fontsize = 12)
plt.ylabel('Reflectance', fontsize = 12)
#plt.title(f'Mixed Spectrum of {1-mixing_ratio} fraction Calcite and {mixing_ratio} fraction Biota', fontsize = 13)
plt.legend(loc= 'upper right')
plt.grid(True)
#plt.savefig(f"Compare_snowball.png", dpi = 300)
plt.show()