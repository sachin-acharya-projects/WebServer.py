import re
from typing import Any, Dict
from urllib.parse import unquote


__all__ = ["extract_route_pattern"]


def extract_route_pattern(pattern: str, string: str) -> Dict[str, str | Any] | None:
    # Removing browser quotes like %20 representing space.
    string = unquote(string)
    # Escape special characters in pattern
    pattern = re.escape(pattern)
    # Add optional trailing slash to the pattern
    pattern += r"/*$"
    # Replace <variable_name> with named capturing group regex
    pattern = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", pattern)
    # Compile the regex pattern
    pattern_regex = re.compile(pattern)
    # Match the pattern against the string
    match = pattern_regex.match(string)
    # Extract variable values
    if match:
        return match.groupdict()
    else:
        return None


if __name__ == "__main__":
    # Test cases
    pattern = "/path/<name>"
    string = "/path/openai"
    output = extract_route_pattern(pattern, string)
    print(output)  # ? Output: {'name': 'openai'}

    pattern = "/<name>:<age>"
    string = "/openai:12"
    output = extract_route_pattern(pattern, string)
    print(output)  # ? Output: {'name': 'openai', 'age': '12'}

    pattern = "/path/next/<name>/<age>"
    string = "/path/next/openai/24"
    output = extract_route_pattern(pattern, string)
    print(output)  # ? Output: {'name': 'openai', 'age': '24'}

    pattern = "/path/sachin/s/a/c/h/i/n/<power>/name/<age>"
    string = "/path/sachin/s/a/c/h/i/n/500/name/24"
    output = extract_route_pattern(pattern, string)
    print(output)  # ? Output: {'power': '500', 'age': '24'}

    pattern = "<username>@<domain>.com"
    string = "sachinacharya@gmail.com"
    output = extract_route_pattern(pattern, string)
    print(output)  # ? {'username': 'sachinacharya', 'domain': 'gmail'}

    pattern = "/path/name"
    string = "/path/name"
    output = extract_route_pattern(pattern, string)
    print(output)  # ? {}

    pattern = "/"
    string = "/path/name"
    output = extract_route_pattern(pattern, string)
    print(output)  # ? None
