from re import match, IGNORECASE
from typing import Union, Literal
import operator

LOWER = "<"
GREATER = ">"
GREATER_OR_EQUALS = ">="
LOWER_OR_EQUALS = "<="
EQUALS = "=="
NOT_EQUALS = "!="

ops = {
    LOWER: operator.lt,
    GREATER: operator.gt,
    EQUALS: operator.eq,
    LOWER_OR_EQUALS: operator.le,
    GREATER_OR_EQUALS: operator.ge,
    NOT_EQUALS: operator.ne
}

def is_url(text: str) -> bool:
    """Returns true or false depending on whether the specified text is a reference."""
    re_pat = r"^((https?|ftp|file)://)?(www\.)?([-A-Za-z0-9+&@#/%?=~_|!:,.;]*)$"
    url_matches = bool(match(re_pat, text, IGNORECASE))
    return url_matches

def contains(text: str, what_contains: Union[str, dict]) -> bool:
    """Returns true if the specified text contains the specified values, and false otherwise. The specified values can be passed as a str or dict."""
    if isinstance(what_contains, str):
        return what_contains in text.lower()
    else:
        for value in what_contains:
            if value.lower() in text.lower():
                return True
        return False

def regexp_matches(text: str, pattern: str, ignore_case: bool = True) -> bool:
    """Returns true if the text matches the regular expression, otherwise False. If "ignore_case" is true, the case is ignored."""
    if not ignore_case:
        return bool(match(pattern, text))
    else:
        return bool(match(pattern, text, IGNORECASE))

def in_range(value: int, minimum: int, maximum: int) -> bool:
    """Returns true if the specified number is within the radius of the minimum and maximum, otherwise returns false"""
    return minimum <= value <= maximum

def length(value: Union[str, int], length: int) -> bool:
    """Returns true if the text number length is equal to the specified length, otherwise false."""
    if isinstance(value, int):
        return len(str(value)) == length
    else:
        return len(value) == length
    
def length_is(value: Union[str, int], length: int, condition = GREATER) -> bool:
    """Returns true if the length of the text or value matches the condition, otherwise false (Conditions can be: GREATER, LOWER, EQUALS, GREATER_OR_EQUALS, LOWER_OR_EQUALS, or NOT_EQUALS)."""
    if isinstance(value, int):
        return ops[condition](len(str(value)), length)
    else:
        return ops[condition](len(value), length)