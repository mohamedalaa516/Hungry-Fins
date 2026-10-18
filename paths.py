import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    RESOURCE_DIR = Path(sys._MEIPASS)
else:
    RESOURCE_DIR = Path(__file__).resolve().parent


def resource_path(*parts):
    return RESOURCE_DIR.joinpath(*parts)


DATA_DIR = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))

SAVE_DIR = DATA_DIR / "Hungry Fins" / "save_slots"
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def save_path(slot):
    return SAVE_DIR / f"save_slot{slot}.json"
