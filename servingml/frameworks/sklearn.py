import os
import joblib

from typing import Union

from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline

from servingml.constants import MODEL_STORE_SKLEARN, MODEL_STORE_SKLEARN_WORKING


SklearnModel = Union[BaseEstimator, Pipeline]


def save_model(model_name: str, model: SklearnModel) -> None:
    if not os.path.exists(MODEL_STORE_SKLEARN):
        os.makedirs(MODEL_STORE_SKLEARN)
    model_path = os.path.join(MODEL_STORE_SKLEARN, f"{model_name}.pkl")
    joblib.dump(model, model_path)


def load_model(model_name: str) -> SklearnModel:
    print("MODEL_STORE_SKLEARN_WORKING", MODEL_STORE_SKLEARN_WORKING)
    model_path = os.path.join(MODEL_STORE_SKLEARN_WORKING, f"{model_name}.pkl")
    if not os.path.exists(model_path):
        raise ValueError(
            f"Model {model_name} is not found at the sklearn model store. Make sure you saved it first."
        )
    return joblib.load(model_path)
