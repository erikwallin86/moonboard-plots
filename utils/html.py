import random


def frame(string):
    return f'<div class=frame>{string}</div>'


def image(string):
    return f"<img src='data:image/png;base64,{string}'/>"


def h2(string):
    return f"<h2>{string}</h2>"


def h4(string):
    return f"<h4>{string}</h4>"


def parse_docstring(obj):
    docstring_list = obj.__doc__.split("\n")
    output = ""
    for part in docstring_list:
        output += part.strip() + " "
    return output


def get_wrong_password_string():
    list_of_messages = [
        "One can't flash every problem",
        "Password flash attempt failed",
        "You dabbed your password. Try again!",
    ]
    return random.choice(list_of_messages)
