# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["OutputMappingUpdateResponse"]


class OutputMappingUpdateResponse(BaseModel):
    id: str

    column_locations: Optional[Dict[str, Dict[str, str]]] = None

    created_at: datetime

    created_by: str

    data_locations: List[str]

    output_data_type: Optional[str] = None

    output_filename: Optional[str] = None

    status: str

    updated_at: datetime
