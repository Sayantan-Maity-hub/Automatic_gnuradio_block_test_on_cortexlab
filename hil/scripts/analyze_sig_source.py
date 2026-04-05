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
    if not results_dir.is_dir():
        print(f"Results dirctory {results_dir} does not exist")
        return 1
    result_files = sorted(results_dir.glob("*_capture_summery.json"))
    if not result_files:
        print("No result files found in {results_dir}")
        return 1
    
    all_results = []
    overall_passed = True
    for file_path in result_files:
        with open(file_path, "r", encoding ="utf-8") as f:
            data = json.load(f)

            result = evaluate_iteration_(data)
            all_results.append(result)

            if not result["passed"]:
                overall_passed = False

            print(f"[{result['iteraion']}] PASS: {result['passed']}")
            print(f" freq_error = {result['metrics']['peak_frequency_error_hz']:.2f} Hz")
            print(f" snr = {result['metrics']['snr_db']:.2f} dB")
            print(f" amp_error = {result['metrics']['relative_amplitude_error']:.2f}")
            print()

            summary = {
                "overall_passed": overall_passed,
                "total_iterations": len(all_results),
                "passed_iterations": sum(1 for r in all_results if r["passed"]),
                "failed_iterations": sum(1 for r in all_results if not r["passed"]),
                "results": all_results,
            }

            with open("hil_analysis_results.json", "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)

                print("------------Final Results------------")
                print(f"Overall PASS: {overall_passed}")
                print("-------------------------------------") 

                return 0 if overall_passed else 2

            if __name__ == "__main__":
                sys.exit(main())
                 
