import json
import subprocess
import sys
from pathlib import Path

SUPPORTED_BLOCKS_MAP ={
    "gr-analog/lib/sig_source_impl.cc": "sig_source",
    "gr-analog/lig/sig_source_impl.h": "sig_source",
}
def run_cmd(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_changed_files(changed_files: list[str]) -> list[str]:
    detected = set()
    for file_path in changed_files:
        normalized = Path(file_path).as_posix()
        block = SUPPORTED_BLOCKS_MAP.get(normalized)
        if block:
            detected.add(block)
    return sorted(detected)

def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "main"
    changed_files = get_changed_files(base_ref)
    detected_blocks = get_changed_files(changed_files)

    result = {
        "base_ref": base_ref,
        "changed_files": changed_files,
        "detected_blocks": detected_blocks
    }
    