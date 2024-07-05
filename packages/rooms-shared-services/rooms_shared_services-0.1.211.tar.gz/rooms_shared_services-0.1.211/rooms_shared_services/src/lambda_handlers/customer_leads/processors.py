import os
from abc import abstractmethod

from rooms_shared_services.src.lambda_handlers.abstract.processors import AbstractLambdaDataProcessor
from rooms_shared_services.src.settings.dynamodb.customer_leads import Settings as CustomerLeadStorageSettings
from rooms_shared_services.src.storage.dynamodb import DynamodbStorageClient
from rooms_shared_services.src.storage.models import BaseDynamodbModel


class AbstractCustomerLeadStorageProcessor(AbstractLambdaDataProcessor):
    storage_client_method: str

    def __init__(self) -> None:
        """Set attributes.

        Raises:
            ValueError: When no key id provided
        """
        key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        if not key_id:
            raise ValueError("No key id")
        storage_settings = CustomerLeadStorageSettings()
        storage_client_params = {
            "tablename": storage_settings.tablename,
            "region_name": storage_settings.region_name,
            "endpoint_url": storage_settings.endpoint_url,
        }
        self.storage_client = self.provide_storage_client(**storage_client_params)
        self.model_item: BaseDynamodbModel | None = None

    def provide_storage_client(self, **storage_client_params):
        return DynamodbStorageClient(**storage_client_params)

    @abstractmethod
    def provide_storage_method_params(self, *args, **kwargs) -> dict:
        ...

    def run(self, *args, **kwargs):
        storage_method = getattr(self.storage_client, self.storage_client_method)
        storage_method_params = self.provide_storage_method_params(*args, **kwargs)
        return storage_method(**storage_method_params)
