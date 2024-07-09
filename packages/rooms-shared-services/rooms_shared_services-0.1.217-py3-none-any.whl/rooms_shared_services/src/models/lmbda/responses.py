from datetime import datetime

from pydantic import BaseModel

from rooms_shared_services.src.storage.models import BaseDynamodbModel


class AbstractLambdaProcessorResponse(BaseModel):
    success: bool
    res: dict


class AbstractLambdaHandlerCallbackResponse(BaseModel):
    success: bool
    res: dict


class IndividualResult(BaseDynamodbModel):
    runner_type: str
    success: bool | None = None
    started_at: datetime
    completed_at: datetime | None = None
    message: dict | None = None
    error: str | None = None


class LambdaEventHandlerResponse(BaseDynamodbModel):
    event_match: bool
    data_model: BaseModel
    handler_type: str | None = None
    processor_result: IndividualResult | None = None
    callback_result: IndividualResult | None = None
