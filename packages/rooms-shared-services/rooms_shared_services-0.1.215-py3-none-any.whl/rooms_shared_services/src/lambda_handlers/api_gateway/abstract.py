from abc import ABC, abstractmethod

from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel

from rooms_shared_services.src.lambda_handlers.api_gateway.abstract import AbstractLambdaDataProcessor
from rooms_shared_services.src.models.lmbda.http import HttpRequestContextData


class AbstractLambdaEventHandler(ABC):
    def __call__(self, event: dict, context: LambdaContext):
        event_model = self.parse_event(event)
        context_model = self.parse_context(context)
        try:
            run_result = self.run(event_model, context_model)
        except ValueError:
            return {
                "statusCode": 400,
            }
        return {"statusCode": 200, "headers": {"Content-Type": "*/*"}, "body": {"result": run_result}}

    @abstractmethod
    def parse_event(self, event: dict) -> BaseModel:
        ...

    def parse_context(self, context: LambdaContext) -> HttpRequestContextData:
        return HttpRequestContextData.model_validate(context.__dict__)

    @abstractmethod
    def provide_data_processor(self) -> AbstractLambdaDataProcessor:
        ...

    @abstractmethod
    def run(self, event_data, context_data) -> dict:
        ...
