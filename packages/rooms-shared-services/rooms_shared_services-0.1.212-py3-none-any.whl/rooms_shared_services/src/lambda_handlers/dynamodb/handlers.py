import logging
from abc import abstractmethod

from pydantic import BaseModel

from rooms_shared_services.src.lambda_handlers.abstract.handlers import AbstractNestedLambdaEventHandler
from rooms_shared_services.src.models.lmbda.dynamdb_stream import DynamodbData, DynamodbStreamEventModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DynamodbStreamEventHandler(AbstractNestedLambdaEventHandler):
    def provide_data_model_array(self, event_model: DynamodbStreamEventModel) -> list[BaseModel | None]:  # type: ignore
        return [self.retrieve_event_data_model(dynamodb_data=record.dynamodb) for record in event_model.Records]

    @abstractmethod
    def retrieve_event_data_model(self, dynamodb_data: DynamodbData) -> BaseModel | None:
        ...
