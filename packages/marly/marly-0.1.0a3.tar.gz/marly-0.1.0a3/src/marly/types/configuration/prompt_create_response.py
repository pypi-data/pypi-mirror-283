# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["PromptCreateResponse", "Message"]


class Message(BaseModel):
    content: str

    role: str


class PromptCreateResponse(BaseModel):
    id: str

    created_at: datetime

    created_by: str

    messages: List[Message]

    name: Optional[str] = None

    prompt_id: Optional[str] = None

    response_format: str

    type: Optional[str] = None

    updated_at: datetime

    variables: object
