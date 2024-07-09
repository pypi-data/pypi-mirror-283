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

__all__ = ["OrchestrationsResource", "AsyncOrchestrationsResource"]


class OrchestrationsResource(SyncAPIResource):
    @cached_property
    def pipelines(self) -> PipelinesResource:
        return PipelinesResource(self._client)

    @cached_property
    def with_raw_response(self) -> OrchestrationsResourceWithRawResponse:
        return OrchestrationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrchestrationsResourceWithStreamingResponse:
        return OrchestrationsResourceWithStreamingResponse(self)


class AsyncOrchestrationsResource(AsyncAPIResource):
    @cached_property
    def pipelines(self) -> AsyncPipelinesResource:
        return AsyncPipelinesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncOrchestrationsResourceWithRawResponse:
        return AsyncOrchestrationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrchestrationsResourceWithStreamingResponse:
        return AsyncOrchestrationsResourceWithStreamingResponse(self)


class OrchestrationsResourceWithRawResponse:
    def __init__(self, orchestrations: OrchestrationsResource) -> None:
        self._orchestrations = orchestrations

    @cached_property
    def pipelines(self) -> PipelinesResourceWithRawResponse:
        return PipelinesResourceWithRawResponse(self._orchestrations.pipelines)


class AsyncOrchestrationsResourceWithRawResponse:
    def __init__(self, orchestrations: AsyncOrchestrationsResource) -> None:
        self._orchestrations = orchestrations

    @cached_property
    def pipelines(self) -> AsyncPipelinesResourceWithRawResponse:
        return AsyncPipelinesResourceWithRawResponse(self._orchestrations.pipelines)


class OrchestrationsResourceWithStreamingResponse:
    def __init__(self, orchestrations: OrchestrationsResource) -> None:
        self._orchestrations = orchestrations

    @cached_property
    def pipelines(self) -> PipelinesResourceWithStreamingResponse:
        return PipelinesResourceWithStreamingResponse(self._orchestrations.pipelines)


class AsyncOrchestrationsResourceWithStreamingResponse:
    def __init__(self, orchestrations: AsyncOrchestrationsResource) -> None:
        self._orchestrations = orchestrations

    @cached_property
    def pipelines(self) -> AsyncPipelinesResourceWithStreamingResponse:
        return AsyncPipelinesResourceWithStreamingResponse(self._orchestrations.pipelines)
