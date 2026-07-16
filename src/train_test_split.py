"""
=========================================
Module : train_test_split.py
Project: KOTTU
Purpose: Split Dataset
=========================================
"""

from sklearn.model_selection import train_test_split


class DatasetSplitter:

    def split(
        self,
        X,
        y,
        test_size=0.2,
        validation_size=0.2,
        random_state=42
    ):

        # First Split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )

        # Second Split
        X_train, X_validation, y_train, y_validation = train_test_split(
            X_train,
            y_train,
            test_size=validation_size,
            random_state=random_state,
            stratify=y_train
        )

        return (
            X_train,
            X_validation,
            X_test,
            y_train,
            y_validation,
            y_test
        )