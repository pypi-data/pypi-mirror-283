# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ModelRetrieveResponse"]


class ModelRetrieveResponse(BaseModel):
    id: str

    additional_params: Dict[str, Optional[str]]

    created_at: datetime

    created_by: str

    api_model_name: str = FieldInfo(alias="model_name")

    api_model_type: str = FieldInfo(alias="model_type")

    updated_at: datetime
