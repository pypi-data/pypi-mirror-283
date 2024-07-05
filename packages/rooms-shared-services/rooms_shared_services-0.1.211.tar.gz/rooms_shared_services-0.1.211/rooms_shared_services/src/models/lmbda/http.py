import json
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, IPvAnyAddress

HttpMethod = Literal["GET", "POST", "PATCH", "DELETE"]

APIGatewayStage = Literal["stage", "prod"]


class HttpRequestEventData(BaseModel):
    method: HttpMethod
    api_id: str
    source_ip: IPvAnyAddress
    stage: APIGatewayStage
    created_at: datetime
    query_string_parameters: dict | None
    path_parameters: dict | None
    payload: dict | None

    @classmethod
    def from_lambda_event(cls, event: dict):
        model_params = {
            "method": event["httpMethod"],
            "api_id": event["requestContext"]["apiId"],
            "source_ip": event["requestContext"]["identity"]["sourceIp"],
            "stage": event["requestContext"]["stage"],
            "created_at": datetime.strptime(event["requestContext"]["requestTime"], "%d/%b/%Y:%H:%M:%S %z"),
            "query_string_parameters": event["queryStringParameters"],
            "path_parameters": event["pathParameters"],
            "payload": event["body"] and json.loads(event["body"]),
        }
        return cls.model_validate(model_params)


class CognitoIdentityData(BaseModel):
    cognito_identity_id: str | None = None
    cognito_identity_pool_id: str | None = None


class HttpRequestContextData(BaseModel):
    function_name: str
    memory_limit_in_mb: int
    function_version: str
    invoked_function_arn: str
    client_context: dict | None
    identity: CognitoIdentityData | None = None
