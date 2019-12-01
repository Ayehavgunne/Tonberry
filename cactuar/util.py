import json
from dataclasses import is_dataclass, asdict
from typing import Dict, Union, Any


class DataClassEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Dict[str, Any]:
        if is_dataclass(obj):
            return asdict(obj)
        return json.JSONEncoder.default(self, obj)


def standardize_data_types(value: Union[str, bytes]) -> str:
    """
    Will convert any byte strings to UTF-8 strings to be more consistant with the other
    paramater passing styles (json). Turns any string that is only composed
    of integers into an int. Turns any string that is convertable to a Decimal or float
    to a Decimal.
    """
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    # if value.isnumeric():
    #     value = int(value)
    # else:
    #     try:
    #         value = decimal.Decimal(value)
    #     except decimal.InvalidOperation:
    #         pass
    return value


def format_data(kwargs: Dict) -> Dict:
    """
    De-lists any single-item lists and scrubs the values

    So {b'foo': [b'bar']} would become {'foo': 'bar'}
    """
    new_kwargs = {}
    for key, value in kwargs.items():
        if isinstance(value, list):
            for index, val in enumerate(value):
                value[index] = standardize_data_types(val)
        if len(value) == 1:
            value = standardize_data_types(value[0])
        new_kwargs[standardize_data_types(key)] = value
    return new_kwargs
