# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["OutputMappingUpdateParams"]


class OutputMappingUpdateParams(TypedDict, total=False):
    created_by: Required[str]

    column_locations: Optional[Dict[str, Dict[str, str]]]

    created_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    data_locations: List[str]

    output_data_type: Optional[str]

    output_filename: Optional[str]

    status: str

    updated_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
