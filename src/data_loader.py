"""
=========================================
Module : data_loader.py
Project: KOTTU
Purpose: Load Keystroke Dynamics Dataset
=========================================
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "DSL-StrongPasswordData.csv"


class DataLoader:

    def __init__(self):
        self.data_path = DATA_PATH

    def load_dataset(self):
        return pd.read_csv(self.data_path)