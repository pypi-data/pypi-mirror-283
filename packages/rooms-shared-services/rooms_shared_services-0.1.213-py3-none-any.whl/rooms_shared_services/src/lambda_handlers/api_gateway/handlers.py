import logging

from aws_lambda_powertools.utilities.typing import LambdaContext

from rooms_shared_services.src.lambda_handlers.abstract.handlers import AbstractLambdaEventHandler
from rooms_shared_services.src.models.lmbda.http import HttpRequestContextData, HttpRequestEventData

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class APIGatewayRequestHandler(AbstractLambdaEventHandler):
    """Handle API GATEWAY requests."""

    def parse_event(self, event: dict) -> HttpRequestEventData:
        return HttpRequestEventData.from_lambda_event(event=event)

    def parse_context(self, context: LambdaContext) -> HttpRequestContextData:
        return HttpRequestContextData.model_validate(context.__dict__)

    def run(self, event_data: HttpRequestEventData, context_data: HttpRequestContextData) -> dict:
        data_processor = self.provide_data_processor()
        return data_processor(event_data, context_data)
