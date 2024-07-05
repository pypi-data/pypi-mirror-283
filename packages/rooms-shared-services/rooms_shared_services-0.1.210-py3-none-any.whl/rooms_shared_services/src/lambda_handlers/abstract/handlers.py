from abc import ABC, abstractmethod
from typing import TypeVar

from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel

from rooms_shared_services.src.lambda_handlers.abstract.callbacks import AbstractLambdaHandlerCallback
from rooms_shared_services.src.lambda_handlers.abstract.processors import AbstractLambdaDataProcessor
from rooms_shared_services.src.models.lmbda.abstract import AbstractLambdaEventModel
from rooms_shared_services.src.models.lmbda.responses import (
    AbstractLambdaHandlerCallbackResponse,
    AbstractLambdaProcessorResponse,
)

LambdaProcessorResponseType = TypeVar("LambdaProcessorResponseType", bound=AbstractLambdaProcessorResponse)
LambdaHandlerCallbackResponseType = TypeVar(
    "LambdaHandlerCallbackResponseType",
    bound=AbstractLambdaHandlerCallbackResponse,
)


# One of the handlers, that must handle a received lambda event.
class AbstractNestedLambdaEventHandler(ABC):
    label: str
    event_data_processor: AbstractLambdaDataProcessor
    callback: AbstractLambdaHandlerCallback
    response: list[dict]
    lambda_context: LambdaContext

    def __init__(self, lambda_context: LambdaContext, *args, **kwargs):
        """Set attributes.

        Parameters:
            lambda_context (LambdaContext): _description_
            args: _description_
            kwargs: _description_
        """
        self.lambda_context = lambda_context
        self.event_data_processor = self.provide_data_processor(*args, **kwargs)
        self.callback = self.provide_callback(*args, **kwargs)
        self.response_array: list = []

    def __call__(self, event_model: AbstractLambdaEventModel):
        self.handle_event_model(event_model)
        return self.response

    def provide_processor_params(self, data_model: BaseModel) -> dict:
        """Convert event_model into processor input params.

        Args:
            data_model (BaseModel): _description_

        Returns:
            dict: _description_
        """
        return data_model.model_dump()

    def handle_data_model(self, data_model: BaseModel | None):
        if data_model is None:
            response = {"event_match": False}
        else:
            response = {}
            self.run_all(data_model, response)
        self.response_array.append(response)

    def handle_event_model(self, event_model: AbstractLambdaEventModel):
        data_model_array = self.provide_data_model_array(event_model)
        for data_model in data_model_array:
            self.handle_data_model(data_model=data_model)

    def run_processor(self, data_model: BaseModel, response: dict) -> dict | None:
        processor_input_params = self.provide_processor_params(data_model=data_model)
        try:
            return self.event_data_processor(response=response, **processor_input_params)
        except Exception as err:
            response.update({"processor": {"error": str(err)}})
            return None

    def run_callback(self, res: dict, response: dict) -> None:
        if self.callback is None:
            response.update({"variant": "callback", "provided": "false"})
        try:
            self.callback(res, response)
        except Exception as err:
            response.update({"variant": "callback", "error": str(err)})

    def run_all(self, data_model: BaseModel, response: dict) -> None:
        processor_result = self.run_processor(data_model=data_model, response=response)
        if "error" in response["processor"]:
            response.update({"variant": "callback", "result": "None"})
        else:
            if processor_result is None:
                raise ValueError("Invalid processor result.")
            self.run_callback(res=processor_result, response=response)

    @abstractmethod
    def provide_data_model_array(self, event_model: AbstractLambdaEventModel):
        ...

    @abstractmethod
    def provide_data_processor(self, *args, **kwargs) -> AbstractLambdaDataProcessor:
        ...

    @abstractmethod
    def provide_callback(self, *args, **kwargs) -> AbstractLambdaHandlerCallback:
        ...


# A combined handler, that must trigger everyone of collected individual handlers.
class AbstractCombinedLambdaEventHandler(ABC):
    handler_types: list[type[AbstractNestedLambdaEventHandler]]

    def __call__(self, event: dict, lambda_context: LambdaContext):
        handler_collection = self.collect_handlers(lambda_context=lambda_context)
        event_model: AbstractLambdaEventModel = self.provide_lambda_event_model(event)
        try:
            handler_results = [lambda_handler(event_model) for lambda_handler in handler_collection]
        except Exception as err:
            return {"error": str(err)}

        return self.provide_lambda_response(handler_results)

    @abstractmethod
    def provide_lambda_event_model(self, event: dict) -> AbstractLambdaEventModel:
        """Validate lambda event model.

        Args:
            event (dict): _description_

        Returns:
            AbstractLambdaEventModel: _description_
        """
        ...

    def collect_handlers(self, lambda_context: LambdaContext) -> list[AbstractNestedLambdaEventHandler]:
        return [handler_type(lambda_context) for handler_type in self.handler_types]

    def provide_lambda_response(self, result_array_list: list[dict]):
        return {
            "handlers": [
                {"name": lambda_handler.label, "result_array": result_array}
                for lambda_handler, result_array in zip(self.handler_types, result_array_list)
            ],
        }
