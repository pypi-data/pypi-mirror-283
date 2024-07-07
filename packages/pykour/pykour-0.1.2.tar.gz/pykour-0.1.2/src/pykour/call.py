import inspect
import json
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict

from pykour.request import Request
from pykour.response import Response
from pykour.schema import BaseSchema


def cast_to_type(value: Any, to_type: type) -> Any:
    if to_type == int:
        return int(value)
    elif to_type == float:
        return float(value)
    elif to_type == bool:
        return value.lower() in ["true", "1", "yes"]
    elif to_type == datetime:
        return datetime.strptime(value, "%Y-%m-%d")
    elif issubclass(to_type, Enum):
        try:
            return to_type[value]
        except KeyError:
            raise ValueError(f"{value} is not a valid {to_type.__name__}")
    elif to_type == dict:
        return json.loads(value)
    else:
        return value


async def call(func: Callable, variables: Dict[str, str], request: Request, response: Response) -> Any:
    sig = inspect.signature(func)
    bound_args: Dict[str, Any] = {}

    for param_name, param in sig.parameters.items():
        if isinstance(param.annotation, type) and issubclass(param.annotation, BaseSchema):
            bound_args[param_name] = param.annotation.from_dict(await request.json())
        elif param.annotation is Request or param_name == "request" or param_name == "req":
            bound_args[param_name] = request
        elif param.annotation is Response or param_name == "response" or param_name == "res" or param_name == "resp":
            bound_args[param_name] = response
        elif param_name in variables:
            bound_args[param_name] = cast_to_type(variables[param_name], param.annotation)

    result = func(**bound_args)

    if inspect.iscoroutine(result):
        return await result
    else:
        return result
