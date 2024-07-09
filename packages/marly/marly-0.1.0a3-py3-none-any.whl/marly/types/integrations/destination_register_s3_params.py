# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DestinationRegisterS3Params"]


class DestinationRegisterS3Params(TypedDict, total=False):
    aws_access_key: Required[str]

    aws_secret_key: Required[str]

    bucket_name: Required[str]

    region_name: Required[str]
