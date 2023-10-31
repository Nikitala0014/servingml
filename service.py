import numpy as np

from typing import Dict, List

from servingml import ModelServer
from servingml.frameworks.sklearn import load_model


class ModelClass(ModelServer):
    def load(self):
        self.model = load_model("iris_clf")

    def predict(self, body: Dict) -> List:
        """Generate model predictions from sample"""
        sample_input = np.asarray(body['inputs'])
        result: np.ndarray = self.model.predict(sample_input)
        return result.tolist()

    def postprocess(self, sample_output: List) -> str:
        """Make postprocessing for returning class name"""
        target_names = ['setosa', 'versicolor', 'virginica']
        # Convert numeric prediction to species name
        predicted_species = target_names[sample_output[0]]
        return predicted_species


model_class = ModelClass(
    model_name="iris_clf",
)

app = model_class.asgi_app
