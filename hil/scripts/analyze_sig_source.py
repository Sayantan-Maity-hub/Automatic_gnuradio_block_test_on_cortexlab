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
    amp_pass = amp_error <= threshold["max_amp_relative_error"]


    passed = freq_pass and snr_pass and amp_pass

    return {
        "iteration": data["iteration"],
        "passed": passed,
        "checks": {
            "frequency": freq_pass,
            "snr": snr_pass,
            "amplitude": amp_pass
        },
        "metrics":{
            "peak_frequency_error_hz": freq_error,
            "snr_db": snr_db,
            "relative_amplitude_error": amp_error,
        },
    }

def main() -> int:
    if len(sys.argv) !=2:
        print("Usage: analyze_sig_source.py <results_dir>")
        return 1
    
    results_dir = path(sys.argv[1])