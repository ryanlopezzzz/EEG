import numpy as np

def get_power_spectrum(time_series):
    """
    Applies window function and fourier transform to time_series data and returns power spectrum of FFT: ps[freq]=|FFT(x)|^2[freq]

    :param time_series: Numpy array containing the most recent ADC voltage difference measurements.
    """
    time_series_zero_mean = time_series-np.mean(time_series)
    time_series_fft = np.fft.fft(time_series_zero_mean)
    ps = np.abs(time_series_fft)**2 #Gets square of complex number
    return ps

def get_rms_voltage(ps, freq_min, freq_max, freq, time_series_len):
    """
    Gets the Root-Mean-Square (RMS) voltage of waves with frequency between freq_min and freq_max. Parseval's Theorem says:
    \sum_{i=0}^{N-1} x[i]^2 = \frac{1}{N} \sum_{i=-(N-1)}^{N-1} |FFT(x)[i]|^2
    Using this, the RMS voltage is (first formula is definition, second is implemented evaluation):
    \sqrt{ \frac{1}{N} \sum_{i=0}^{N-1} x[i]^2 } = \frac{1}{N} \sqrt{ \sum_{freq in range} |FFT(x)[freq]|^2}
    
    :param ps: FFT power spectrum of time_series, ps[freq] = |FFT(x)|^2[freq].
    :param freq_min: Number corresponding to minimum alpha wave frequency in Hz.
    :param freq_max: Number corresponding to maximum alpha wave frequency in Hz.
    :param freq: Numpy array of negative and positive FFT freq, fft.fftfreq of time_series
    :param time_series_len: Integer length of time_series
    """
    freq_abs = np.abs(freq) 
    ps_in_range = ps[(freq_abs <= freq_max) & (freq_abs >= freq_min)] #Gets power spectrum for freq in range [freq_min, freq_max]
    rms = (1/time_series_len) * np.sqrt(np.sum(ps_in_range))
    return rms


