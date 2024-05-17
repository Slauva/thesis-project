import json
from typing import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import cumtrapz, simps
from scipy.signal import butter, filtfilt, iirnotch, spectrogram, welch


class EmgPreprocessing:

    def __init__(self, filepath: str, pointspath: str) -> None:
        data = pd.read_csv(filepath)