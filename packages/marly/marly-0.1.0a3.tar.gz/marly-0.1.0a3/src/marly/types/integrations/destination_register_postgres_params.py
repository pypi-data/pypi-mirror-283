# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DestinationRegisterPostgresParams"]


class DestinationRegisterPostgresParams(TypedDict, total=False):
    database: Required[str]

    host: Required[str]

    password: Required[str]

    port: Required[int]

    user: Required[str]

    schema: str
