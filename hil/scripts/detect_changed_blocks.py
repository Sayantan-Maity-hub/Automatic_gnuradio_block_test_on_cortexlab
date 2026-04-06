import json
import subprocess
import sys
from pathlib import Path

SUPPORTED_BLOCKS_MAP ={
    "gr-analog/lib/sig_source_impl.cc": "sig_source",
    "gr-analog/lig/sig_source_impl.h": "sig_source",
}
