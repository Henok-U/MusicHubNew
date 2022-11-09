import random
import string

from rest_framework.pagination import PageNumberPagination


def trim_spaces_from_data(data: str) -> str:
    """
    trim all whitespace characters from given string
    """
    for key, value in data.items():
        data[key] = " ".join(value.split())
    return data


def get_random_string(length: int) -> str:
    """
    returns random asci lowercase string with given length
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class LargeResultsSetPagination(PageNumberPagination):
    """
    Overrides default pagination class provided in settings.py,
    inside REST_FRAMEWORK dictionary.
    """

    page_size = 40
    page_size_query_parameter = "page_size"
    max_page_size = 40


def format_sec_to_mins(sec: int) -> str:
    """
    Format seconds to '%m%m:%s%s'
    """
    try:
        return f"{sec // 60}:{sec % 60}"
    except TypeError:
        return "unknown"
