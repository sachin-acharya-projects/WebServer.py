import re
from typing import Any, Dict
from urllib.parse import unquote


__all__ = ['extract_route_pattern']

def extract_route_pattern(pattern: str, string: str) -> Dict[str, str | Any] | None:
    # Removing browser quotes like %20 representing space.
    string = unquote(string)
    # Escape special characters in pattern
    pattern = re.escape(pattern)
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
    pattern1 = "/path/<name>"
    string1 = "/path/openai"
    output1 = extract_route_pattern(pattern1, string1)
    print(output1)  #? Output: {'name': 'openai'}

    pattern2 = "/<name>:<age>"
    string2 = "/openai:12"
    output2 = extract_route_pattern(pattern2, string2)
    print(output2)  #? Output: {'name': 'openai', 'age': '12'}

    pattern3 = "/path/next/<name>/<age>"
    string3 = "/path/next/openai/24"
    output3 = extract_route_pattern(pattern3, string3)
    print(output3)  #? Output: {'name': 'openai', 'age': '24'}

    pattern4 = "/path/sachin/s/a/c/h/i/n/<power>/name/<age>"
    string4 = "/path/sachin/s/a/c/h/i/n/500/name/24"
    output4 = extract_route_pattern(pattern4, string4)
    print(output4)  #? Output: {'power': '500', 'age': '24'}


    pattern5 = "<username>@<domain>.com"
    string5 = "sachinacharya@gmail.com"
    output5 = extract_route_pattern(pattern5, string5)
    print(output5)