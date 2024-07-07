# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["PipelineCreateParams"]


class PipelineCreateParams(TypedDict, total=False):
    created_by: Required[str]

    model_id: Required[str]

    name: Required[str]

    pipeline_schema_id: Required[str]

    run_type: Required[str]

    created_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    integrations: Dict[str, str]

    normalization_id: str

    prompt_ids: Dict[str, str]

    status: str

    updated_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
