#   ---------------------------------------------------------------------------------
#   Copyright (c) Hexafuchs. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This provides helpers to convert data."""

__all__ = ["to_snake_case", "dict_keys_to_snake_case"]

from typing import TypeVar

T = TypeVar("T")


def to_snake_case(camel_case_str: str) -> str:
    return "".join(map(lambda e: "_" + e.lower() if e.isupper() else e, list(camel_case_str)))


def dict_keys_to_snake_case(data: T) -> T:
    if type(data) is list:
        return [dict_keys_to_snake_case(e) for e in data]
    if type(data) is not dict:
        return data
    return {to_snake_case(key): dict_keys_to_snake_case(value) for key, value in data.items()}
