import sys
import json


def get_next_json():
    current_char = sys.stdin.read(1)
    while current_char.isspace():
        current_char = sys.stdin.read(1)
    if not current_char:
        return ""
    json_val = [current_char]
    if current_char == "{":
        find_json_object(json_val)
    elif current_char == "[":
        find_array(json_val)
    elif current_char == '"':
        find_string(json_val)
    elif not current_char.isspace():
        find_nonwhite_space(json_val)

    return json.loads("".join(json_val))


def find_json_object(existing_json):
    num_braces = 1
    while num_braces != 0:
        current_char = sys.stdin.read(1)
        existing_json.append(current_char)
        if current_char == "{":
            num_braces += 1
        elif current_char == "}":
            num_braces -= 1
        elif current_char == '"':
            find_string(existing_json)


def find_array(existing_json):
    num_braces = 1
    while num_braces != 0:
        current_char = sys.stdin.read(1)
        existing_json.append(current_char)
        if current_char == "[":
            num_braces += 1
        elif current_char == "]":
            num_braces -= 1
        elif current_char == '"':
            find_string(existing_json)


def find_string(existing_json):
    current_char = sys.stdin.read(1)
    existing_json.append(current_char)
    while current_char != '"':
        if current_char == "\\":
            current_char = sys.stdin.read(1)
            existing_json.append(current_char)
        current_char = sys.stdin.read(1)
        existing_json.append(current_char)


def find_nonwhite_space(existing_json):
    current_char = sys.stdin.read(1)
    existing_json.append(current_char)
    while (not current_char.isspace()) and current_char != "":
        current_char = sys.stdin.read(1)
        existing_json.append(current_char)


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


if __name__ == '__main__':
    json_input = get_next_json()
    while json_input != "":
        print(json.dumps(reverse_json(json_input)))
        json_input = get_next_json()
