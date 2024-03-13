import numpy as np
from scipy.signal import butter, filtfilt, iirnotch


def emg_preprocessing(
    t: np.ndarray,
    y: np.ndarray,
    *,
    sfreq: int = 1000,
    t_baseline: float = None,
    c_baseline: bool = False,
    l_pass: int = None,
    h_band: int = None,
    l_band: int = None,
    notch: int = None,
):
    data = y.copy()
    interval = t.copy()

    # Baseline Correction
    if t_baseline is not None:
        baseline_idx = np.argwhere(t >= t_baseline)[0][0]
        baseline = data[:baseline_idx]
        y0 = np.mean(baseline)
    else:
        y0 = np.mean(data)

    data = data - y0

    # Crop Baseline
    if c_baseline:
        data = data[baseline_idx:]
        interval = interval[baseline_idx:]

    # Band-pass Filter
    if l_band is not None and h_band is not None:
        high = h_band / (sfreq / 2)
        low = l_band / (sfreq / 2)
        b, a = butter(4, [high, low], btype="bandpass")
        data = filtfilt(b, a, data)

    # Rectification
    data = np.abs(data)

    # Low-pass Filter
    if l_pass is not None:
        low = l_pass / (sfreq / 2)
        b, a = butter(4, low, btype="lowpass")
        data = filtfilt(b, a, data)

    # Notch Filter
    if notch in [50, 60]:
        b, a = iirnotch(notch, 30.0, sfreq)

    return interval, data
