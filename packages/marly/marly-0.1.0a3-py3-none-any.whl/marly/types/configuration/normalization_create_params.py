# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["NormalizationCreateParams"]


class NormalizationCreateParams(TypedDict, total=False):
    created_by: Required[str]

    name: Required[str]

    normalization_type: Required[str]

    output_data_source: Required[str]

    output_filename: Required[str]

    additional_params: Dict[str, Optional[str]]

    created_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    description: Optional[str]

    updated_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
