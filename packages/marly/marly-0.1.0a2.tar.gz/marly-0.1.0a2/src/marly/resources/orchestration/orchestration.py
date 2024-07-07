# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from .pipelines import (
    PipelinesResource,
    AsyncPipelinesResource,
    PipelinesResourceWithRawResponse,
    AsyncPipelinesResourceWithRawResponse,
    PipelinesResourceWithStreamingResponse,
    AsyncPipelinesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["OrchestrationResource", "AsyncOrchestrationResource"]


class OrchestrationResource(SyncAPIResource):
    @cached_property
    def pipelines(self) -> PipelinesResource:
        return PipelinesResource(self._client)

    @cached_property
    def with_raw_response(self) -> OrchestrationResourceWithRawResponse:
        return OrchestrationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrchestrationResourceWithStreamingResponse:
        return OrchestrationResourceWithStreamingResponse(self)


class AsyncOrchestrationResource(AsyncAPIResource):
    @cached_property
    def pipelines(self) -> AsyncPipelinesResource:
        return AsyncPipelinesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncOrchestrationResourceWithRawResponse:
        return AsyncOrchestrationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrchestrationResourceWithStreamingResponse:
        return AsyncOrchestrationResourceWithStreamingResponse(self)


class OrchestrationResourceWithRawResponse:
    def __init__(self, orchestration: OrchestrationResource) -> None:
        self._orchestration = orchestration

    @cached_property
    def pipelines(self) -> PipelinesResourceWithRawResponse:
        return PipelinesResourceWithRawResponse(self._orchestration.pipelines)


class AsyncOrchestrationResourceWithRawResponse:
    def __init__(self, orchestration: AsyncOrchestrationResource) -> None:
        self._orchestration = orchestration

    @cached_property
    def pipelines(self) -> AsyncPipelinesResourceWithRawResponse:
        return AsyncPipelinesResourceWithRawResponse(self._orchestration.pipelines)


class OrchestrationResourceWithStreamingResponse:
    def __init__(self, orchestration: OrchestrationResource) -> None:
        self._orchestration = orchestration

    @cached_property
    def pipelines(self) -> PipelinesResourceWithStreamingResponse:
        return PipelinesResourceWithStreamingResponse(self._orchestration.pipelines)


class AsyncOrchestrationResourceWithStreamingResponse:
    def __init__(self, orchestration: AsyncOrchestrationResource) -> None:
        self._orchestration = orchestration

    @cached_property
    def pipelines(self) -> AsyncPipelinesResourceWithStreamingResponse:
        return AsyncPipelinesResourceWithStreamingResponse(self._orchestration.pipelines)
