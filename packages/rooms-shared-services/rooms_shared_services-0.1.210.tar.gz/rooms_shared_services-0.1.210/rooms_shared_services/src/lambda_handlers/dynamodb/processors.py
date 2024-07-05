from rooms_shared_services.src.lambda_handlers.abstract.processors import AbstractLambdaDataProcessor
from rooms_shared_services.src.storage.models import BaseDynamodbModel


class BaseDynamodbStreamEventProcessor(AbstractLambdaDataProcessor):
    model_class: BaseDynamodbModel

    def __init__(self):
        """Set items."""
        self.new_item: BaseDynamodbModel | None = None
        self.old_item: BaseDynamodbModel | None = None

    def __call__(
        self,
        keys: dict,
        new_image: dict | None = None,
        old_image: dict | None = None,
        **kwargs,
    ):  # noqa: N803
        for data_dict, attr in zip([new_image, old_image], ["new_item", "old_item"]):
            if data_dict:
                setattr(self, attr, self.validate_model(model_data=data_dict, keys=keys))
        res = super().__call__()
        self.reset()
        return res

    def reset(self):
        self.new_item = None
        self.old_item = None

    def validate_model(self, model_data: dict, keys: dict):
        model_data.update(keys)
        return self.model_class.validate_dynamodb_item(data_dict=model_data, from_raw=True)
