# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ModelCreateParams"]


class ModelCreateParams(TypedDict, total=False):
    api_key: Required[str]

    created_by: Required[str]

    model_name: Required[str]

    model_type: Required[str]

    additional_params: Dict[str, Optional[str]]

    created_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    updated_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
