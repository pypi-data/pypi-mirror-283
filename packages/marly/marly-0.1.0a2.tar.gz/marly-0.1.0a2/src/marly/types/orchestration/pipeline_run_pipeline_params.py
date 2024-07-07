# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["PipelineRunPipelineParams"]


class PipelineRunPipelineParams(TypedDict, total=False):
    filenames: Required[List[str]]

    output_mapping_ids: Required[List[str]]

    pipeline_id: Required[str]
