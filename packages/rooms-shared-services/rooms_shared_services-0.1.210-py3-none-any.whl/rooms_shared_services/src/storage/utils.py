import json
import logging
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

type_serializer = TypeSerializer()
type_deserializer = TypeDeserializer()


def dump_value_dict(data_dict: dict, dynamodb_format: bool = False, json_format: bool = False) -> str | dict:
    """Convert a data dict to a dynamodb supported dict format or a json dump of this dict.

    Args:
        data_dict (dict): _description_
        dynamodb_format (bool): _description_. Defaults to False.
        json_format (bool): _description_. Defaults to False.

    Returns:
        str | dict: _description_
    """
    data_dict = {
        item_key: formatted_value
        for item_key, item_value in data_dict.items()
        if (formatted_value := convert_to_supported_format(item_value)) is not None
    }
    if dynamodb_format:
        data_dict = {item_key: serialize_value(item_value) for item_key, item_value in data_dict.items()}
    if json_format:
        return convert_to_json(data_dict)
    return data_dict


def load_value_json(value_json: str) -> dict:
    """Convert a json-serialized dict to a normal dict.

    Args:
        value_json (str): _description_

    Returns:
        dict: _description_
    """
    value_dict = json.loads(value_json)
    return parse_serialized_dict(value_dict=value_dict)


def parse_serialized_dict(value_dict: dict) -> dict:
    """Convert a dynamodb item value dict with dynamodb datatype symbols to a regular dict without datatype symbols.

    Args:
        value_dict (dict): _description_

    Returns:
        dict: _description_
    """
    value_dict = {item_key: type_deserializer.deserialize(item_value) for item_key, item_value in value_dict.items()}
    return {item_key: convert_from_supported_formats(item_value) for item_key, item_value in value_dict.items()}


def convert_from_supported_formats(item_value: Any) -> Any:
    """Convert a value in supported Dynamodb format to a more regular datatype format.

    Args:
        item_value (Any): _description_

    Returns:
        Any: _description_
    """
    match item_value:
        case Decimal():
            float_value = float(item_value)
            int_value = int(item_value)
            if float_value == int_value:
                converted_value = int_value
            else:
                converted_value = float_value
        case _:
            converted_value = item_value
    return converted_value


def convert_to_json(data_dict: dict) -> str:
    """Convert a data dict to a json str.

    Args:
        data_dict (dict): _description_

    Returns:
        str: _description_
    """
    return json.dumps(data_dict, indent=4)


def serialize_value(item_value: Any) -> dict:
    """Convert an item value to a dict with dynamodb supported datatype symbol as a key.

    Args:
        item_value (Any): _description_

    Returns:
        dict: _description_
    """
    return type_serializer.serialize(item_value)


def convert_to_supported_format(item_value: Any) -> str | list | Decimal | set | dict:
    """Convert an arbitrary value to a supported by DynamoDB format.

    Args:
        item_value (Any): _description_

    Returns:
        Any: _description_
    """
    match item_value:
        case Enum():
            formatted_value = item_value.value
        case UUID():
            formatted_value = str(item_value)
        case float():
            formatted_value = Decimal(str(item_value))
        case datetime():
            formatted_value = item_value.isoformat()
        case list():
            formatted_value = [convert_to_supported_format(item_value_elem) for item_value_elem in item_value]
        case set():
            formatted_value = {convert_to_supported_format(item_value_elem) for item_value_elem in item_value}
        case dict():
            formatted_value = {
                item_value_key: convert_to_supported_format(item_value_value)
                for item_value_key, item_value_value in item_value.items()
            }
        case _:
            formatted_value = item_value
    return formatted_value
