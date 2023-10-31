from typing import Dict, Any
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
import logging

class ModelServer:
    """Class that creates a Starlette app for serving a machine learning model."""
    
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.model = self.load()
        logging.basicConfig(level=logging.INFO)

    @property
    def asgi_app(self) -> Starlette:
        return Starlette(routes=[
            Route(f"/v2/models/{self.model_name}/infer", self._predict_fn, methods=["POST"]),
        ])

    async def _predict_fn(self, request: Request) -> JSONResponse:
        """Handler for the Starlette application."""
        try:
            data = await request.json()
            if not data:
                return JSONResponse({"error": "Invalid input data"}, status_code=400)
            processed_data = self.preprocess(data)
            prediction = self.predict(processed_data)
            result = self.postprocess(prediction)
            return JSONResponse({"result": result})
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return JSONResponse({"error": "Error processing request"}, status_code=500)

    def load(self) -> Any:
        """Model loading operation."""
        raise NotImplementedError()

    def preprocess(self, body: Dict) -> Any:
        """Preprocess the event body before validation and action."""
        return body

    def postprocess(self, result: Any) -> Any:
        """Postprocess the prediction before returning response."""
        return result

    def predict(self, data: Any) -> Any:
        """Model prediction operation."""
        raise NotImplementedError()
