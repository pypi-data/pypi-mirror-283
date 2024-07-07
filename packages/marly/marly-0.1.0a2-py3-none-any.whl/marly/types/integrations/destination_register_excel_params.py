# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DestinationRegisterExcelParams"]


class DestinationRegisterExcelParams(TypedDict, total=False):
    data_source: Required[str]

    output_filename: Required[str]
