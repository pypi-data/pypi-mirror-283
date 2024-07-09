import logging
from typing import Literal, TypeVar

from pydantic import BaseModel

from rooms_shared_services.src.models.lmbda.abstract import AbstractLambdaEventModel
from rooms_shared_services.src.storage.models import BaseDynamodbModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)


ImageVariant = Literal["new", "old"]
StreamViewType = Literal["KEYS_ONLY", "NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES"]
DynamodbStreamModelType = TypeVar("DynamodbStreamModelType", bound=BaseDynamodbModel)


class DynamodbStreamRecord(BaseModel):
    keys: dict
    new_image: dict | None = None
    old_image: dict | None = None
    stream_view_type: str

    @classmethod
    def from_lambda_event(cls, record: dict):
        record_params = {
            "keys": record["Keys"],
            "new_image": record["NewImage"] if "NewImage" in record else None,
            "old_image": record["OldImage"] if "OldImage" in record else None,
            "stream_view_type": record["StreamViewType"],
        }
        return cls.model_validate(record_params)


class DynamodbStreamContextData(BaseModel):
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: str
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: str | None = None
    client_context: str | None = None

    @classmethod
    def from_context_object(cls, context_obj):
        return cls.model_validate(context_obj.__dict__)


class DynamodbData(BaseModel):
    Keys: dict
    NewImage: dict | None
    OldImage: dict | None
    SequenceNumber: int
    SizeBytes: int
    StreamViewType: str

    def from_stream_image(
        self,
        image_variant: ImageVariant,
        model_type: type[DynamodbStreamModelType],
    ) -> DynamodbStreamModelType | None:
        match image_variant:
            case "new":
                item_image = self.NewImage
            case "old":
                item_image = self.OldImage
            case _:
                raise ValueError("Invalid image variant")
        if item_image is None:
            return None
        item_data = {**self.Keys, **item_image}
        return model_type.validate_dynamodb_item(data_dict=item_data, from_raw=True)


class DynamodbRecord(BaseModel):
    eventID: int
    eventName: str
    eventVersion: str
    eventSource: str  # ex: "aws:dynamodb"
    awsRegion: str  # "us-east-1"
    dynamodb: DynamodbData
    eventSourceARN: str  # ex: "stream-ARN"


class DynamodbStreamEventModel(AbstractLambdaEventModel):
    Records: list[DynamodbRecord]

    @classmethod
    def from_lambda_event(cls, event: dict):
        return cls.model_validate(event)
