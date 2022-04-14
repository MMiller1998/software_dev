import json


def get_next_json(reader) -> str:
    current_char = reader.read(1).decode()
    while current_char.isspace():
        current_char = reader.read(1).decode()
    if not current_char:
        return ""
    json_val = [current_char]
    if current_char == "{":
        find_json(json_val, reader)
    elif current_char == "[":
        find_array(json_val, reader)
    elif current_char == '"':
        find_string(json_val, reader)
    elif not current_char.isspace():
        find_nonwhite_space(json_val, reader)

    return _try_json("".join(json_val))


def find_json(existing_json, reader):
    num_braces = 1
    while num_braces != 0:
        current_char = reader.read(1).decode()
        existing_json.append(current_char)
        if current_char == "{":
            num_braces += 1
        elif current_char == "}":
            num_braces -= 1
        elif current_char == '"':
            find_string(existing_json, reader)


def find_array(existing_json, reader):
    num_braces = 1
    while num_braces != 0:
        current_char = reader.read(1).decode()
        existing_json.append(current_char)
        if current_char == "[":
            num_braces += 1
        elif current_char == "]":
            num_braces -= 1
        elif current_char == '"':
            find_string(existing_json, reader)


def find_string(existing_json, reader):
    current_char = reader.read(1).decode()
    existing_json.append(current_char)
    while current_char != '"':
        if current_char == "\\":
            current_char = reader.read(1).decode()
            existing_json.append(current_char)
        current_char = reader.read(1).decode()
        existing_json.append(current_char)


def find_nonwhite_space(existing_json, reader):
    current_char = reader.read(1).decode()
    existing_json.append(current_char)
    while (not current_char.isspace()) and current_char != "":
        current_char = reader.read(1).decode()
        existing_json.append(current_char)


def _try_json(json_str):
    try:
        return json.loads(json_str)
    except (ValueError, json.JSONDecodeError):
        return None


def reverse_json(json):
    if type(json) is int or type(json) is float:
        return json * -1
    elif type(json) is str:
        return json[::-1]
    elif type(json) is bool:
        return not json
    elif type(json) is list:
        json_output = []
        for element in json[::-1]:
            json_output.append(reverse_json(element))
        return json_output
    elif type(json) is dict:
        json_output = {}
        for key, value in json.items():
            json_output[key] = reverse_json(value)
        return json_output
    else:
        return json
