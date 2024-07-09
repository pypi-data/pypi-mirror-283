# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["NormalizationUpdateResponse"]


class NormalizationUpdateResponse(BaseModel):
    id: str

    additional_params: Dict[str, Optional[str]]

    created_at: datetime

    created_by: str

    description: Optional[str] = None

    name: str

    normalization_type: str

    output_data_source: str

    output_filename: str

    updated_at: datetime
