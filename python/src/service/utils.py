from flask import request, jsonify
import json
from marshmallow import Schema, fields, ValidationError
from typing import Dict, Callable
from logging import getLogger

LOGGER = getLogger(__name__)

REQUEST_VALIDATION_MAP: Dict[str, str] = {
    "request_schema_args": "args",
    "request_schema_body": "json"
}


def route_config(params: Dict) -> Callable:
    def wrapper(func: Callable) -> Callable:
        def inner_func(*args, **kwargs):
            # perform request validations
            if any([key in params for key in REQUEST_VALIDATION_MAP.keys()]):
                key = filter(lambda x: x in REQUEST_VALIDATION_MAP.keys(), params.keys())[0]
                request_data = getattr(request, REQUEST_VALIDATION_MAP[key])
                if isinstance(request_data, str):
                    try:
                        request_data = json.loads(request_data)
                        # Validate request body against schema data types
                        params.get(key)().load(request_data)
                    except json.decoder.JSONDecodeError as e:
                        LOGGER.error(f"Invalid Request; Expected json str: {request_data}", e)
                        return jsonify(e.messages), 400
                    except ValidationError as e:
                        LOGGER.error(f"Invalid Request; Doesn't conform to schema: {request_data}", e)
                        return jsonify(e.messages), 400
                elif isinstance(request_data, dict):
                    try:
                        # Validate request body against schema data types
                        params.get(key)().load(request_data)
                    except ValidationError as e:
                        LOGGER.error(f"Invalid Request; Doesn't conform to schema: {request_data}", e)
                        return jsonify(e.messages), 400

            try:
                resp = func(*args, **kwargs)
            except RuntimeError as e:
                LOGGER.error("Encountered exception during routing ", e)
                return jsonify(e.messages), 500

            # perform response validations
            if params.get("response_schema"):
                if isinstance(resp, str):
                    try:
                        resp = json.loads(resp)
                        # Validate response body against schema data types
                        params.get("response_schema")().load(resp)
                    except json.decoder.JSONDecodeError as e:
                        LOGGER.error(f"Invalid Response; Expected json str: {resp}", e)
                        return jsonify(e.messages), 400
                    except ValidationError as e:
                        LOGGER.error(f"Invalid Response; doesn't conform to schema: {resp}", e)
                        return jsonify(e.messages), 400
                    return resp, params.get("code_on_success", 200)
                elif isinstance(resp, dict):
                    try:
                        # Validate response body against schema data types
                        params.get("response_schema")().load(resp)
                    except ValidationError as e:
                        LOGGER.error(f"Invalid Response; doesn't conform to schema: {resp}", e)
                        return jsonify(e.messages), 400
                    return jsonify(resp), params.get("code_on_success", 200)
                else:
                    return jsonify("Invalid response type received from service"), 400
                return resp, params.get("code_on_success", 200)

        # Apply the XXXXX.route decorator
        if params.get("route") is None or params.get("blueprint") is None:
            raise RuntimeError("No 'blueprint' or 'route' specified with config")

        inner_func.__name__ = func.__name__
        decorated = params.get("blueprint").route(params.get("route"))(inner_func)

        return decorated
    return wrapper
