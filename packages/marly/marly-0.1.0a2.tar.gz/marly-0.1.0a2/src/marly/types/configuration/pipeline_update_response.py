# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PipelineUpdateResponse"]


class PipelineUpdateResponse(BaseModel):
    id: str

    created_at: datetime

    created_by: str

    integrations: Dict[str, str]

    api_model_id: str = FieldInfo(alias="model_id")

    name: str

    normalization_id: str

    pipeline_schema_id: str

    prompt_ids: Dict[str, str]

    run_type: str

    status: str

    updated_at: datetime
