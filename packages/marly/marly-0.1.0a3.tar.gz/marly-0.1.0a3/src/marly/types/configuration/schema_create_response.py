# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from datetime import datetime

from ..._models import BaseModel

__all__ = ["SchemaCreateResponse"]


class SchemaCreateResponse(BaseModel):
    id: str

    created_at: datetime

    created_by: str

    keywords: Dict[str, str]

    status: str

    updated_at: datetime
