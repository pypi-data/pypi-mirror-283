# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["PromptUpdateParams", "Message"]


class PromptUpdateParams(TypedDict, total=False):
    path_prompt_id: Required[Annotated[str, PropertyInfo(alias="prompt_id")]]

    created_by: Required[str]

    messages: Required[Iterable[Message]]

    created_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    name: Optional[str]

    body_prompt_id: Annotated[Optional[str], PropertyInfo(alias="prompt_id")]

    response_format: str

    type: Optional[str]

    updated_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    variables: object


class Message(TypedDict, total=False):
    content: Required[str]

    role: Required[str]
