import json
import math
import sys
from pathlib import Path

def relative_error(measured: float, expected: float) -> float:
    if expected == 0:
        return 0.0 if measured == 0 else math.inf
    return abs(measured - expected)/abs(expected)

def evaluate_iteration_(data: dict) -> dict:
    expected = data["expected"]
    measured = data["measured"]
    threshold = data["threshold"]

    expected_freq = expected["tone_freq"]
    measured_freq = measured["peak_freq"]
    expected_amp = expected["ampllitude"]
    measured_amp = measured["amplitude"]
    snr_db = measured["snr_db"]

    freq_error = abs(measured_freq - expected_freq)
    amp_error = relative_error(measured_amp, expected_amp)

    freq_pass = freq_error <= threshold["freq_error_hz"]
    snr_pass = snr_db >= threshold["min_detected_snr_db"]


    passed = freq_pass and snr_