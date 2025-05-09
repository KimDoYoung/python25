from lib.core.datatypes.kavana_datatype import KavanaDataType, String

def deep_primitive(value):
    from lib.core.token import Token
    if isinstance(value, KavanaDataType):
        return deep_primitive(value.primitive)
    # if isinstance(value, Token):
    #     return value.data.string if hasattr(value.data, "string") else str(value.data)
    elif isinstance(value, list):
        return [deep_primitive(v) for v in value]
    elif isinstance(value, dict):
        return {k: deep_primitive(v) for k, v in value.items()}
    else:
        return value

def deep_string(value):
    if isinstance(value, KavanaDataType):
        if isinstance(value, String):
            return f"'{value.string}'"
        else:
            return value.string
    elif isinstance(value, list):
        return "[" + ", ".join(deep_string(v) for v in value) + "]"
    elif isinstance(value, dict):
        return "{" + ", ".join(f"{k}: {deep_string(v)}" for k, v in value.items()) + "}"
    else:
        return str(value)

def deep_token_string(value):
    from lib.core.token import Token
    if isinstance(value, Token):
        return value.data.string if hasattr(value.data, "string") else str(value.data)
    elif isinstance(value, list):
        return "[" + ", ".join(deep_token_string(v) for v in value) + "]"
    elif isinstance(value, dict):
        return "{" + ", ".join(f"'{k}': {deep_token_string(v)}" for k, v in value.items()) + "}"
    else:
        # return str(value)
        return deep_string(value)
