# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import orchestration_run_pipeline_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)

__all__ = ["OrchestrationResource", "AsyncOrchestrationResource"]


class OrchestrationResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OrchestrationResourceWithRawResponse:
        return OrchestrationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrchestrationResourceWithStreamingResponse:
        return OrchestrationResourceWithStreamingResponse(self)

    def run_pipeline(
        self,
        *,
        filenames: List[str],
        output_mapping_ids: List[str],
        pipeline_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        run pipeline given a set of parameters and operation files

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/orchestration/run-pipeline",
            body=maybe_transform(
                {
                    "filenames": filenames,
                    "output_mapping_ids": output_mapping_ids,
                    "pipeline_id": pipeline_id,
                },
                orchestration_run_pipeline_params.OrchestrationRunPipelineParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncOrchestrationResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOrchestrationResourceWithRawResponse:
        return AsyncOrchestrationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrchestrationResourceWithStreamingResponse:
        return AsyncOrchestrationResourceWithStreamingResponse(self)

    async def run_pipeline(
        self,
        *,
        filenames: List[str],
        output_mapping_ids: List[str],
        pipeline_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        run pipeline given a set of parameters and operation files

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/orchestration/run-pipeline",
            body=await async_maybe_transform(
                {
                    "filenames": filenames,
                    "output_mapping_ids": output_mapping_ids,
                    "pipeline_id": pipeline_id,
                },
                orchestration_run_pipeline_params.OrchestrationRunPipelineParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class OrchestrationResourceWithRawResponse:
    def __init__(self, orchestration: OrchestrationResource) -> None:
        self._orchestration = orchestration

        self.run_pipeline = to_raw_response_wrapper(
            orchestration.run_pipeline,
        )


class AsyncOrchestrationResourceWithRawResponse:
    def __init__(self, orchestration: AsyncOrchestrationResource) -> None:
        self._orchestration = orchestration

        self.run_pipeline = async_to_raw_response_wrapper(
            orchestration.run_pipeline,
        )


class OrchestrationResourceWithStreamingResponse:
    def __init__(self, orchestration: OrchestrationResource) -> None:
        self._orchestration = orchestration

        self.run_pipeline = to_streamed_response_wrapper(
            orchestration.run_pipeline,
        )


class AsyncOrchestrationResourceWithStreamingResponse:
    def __init__(self, orchestration: AsyncOrchestrationResource) -> None:
        self._orchestration = orchestration

        self.run_pipeline = async_to_streamed_response_wrapper(
            orchestration.run_pipeline,
        )
