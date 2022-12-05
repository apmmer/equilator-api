import sys
from pathlib import Path

str_base_path = str(Path(__file__).resolve().parent)
paths = sys.path
if str_base_path not in paths:
    sys.path.insert(0, str_base_path)
