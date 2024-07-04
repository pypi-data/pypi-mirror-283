from glob import glob
from pathlib import Path

_current_path = Path(__file__).parent.resolve()
RULE_PATHS = glob(str(_current_path / "**/*.json"), recursive=True)


__version__ = "0.1.0"
