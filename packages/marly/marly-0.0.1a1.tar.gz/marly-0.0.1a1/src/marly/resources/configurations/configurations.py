# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .prompts import (
    PromptsResource,
    AsyncPromptsResource,
    PromptsResourceWithRawResponse,
    AsyncPromptsResourceWithRawResponse,
    PromptsResourceWithStreamingResponse,
    AsyncPromptsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .normalizations import (
    NormalizationsResource,
    AsyncNormalizationsResource,
    NormalizationsResourceWithRawResponse,
    AsyncNormalizationsResourceWithRawResponse,
    NormalizationsResourceWithStreamingResponse,
    AsyncNormalizationsResourceWithStreamingResponse,
)

__all__ = ["ConfigurationsResource", "AsyncConfigurationsResource"]


class ConfigurationsResource(SyncAPIResource):
    @cached_property
    def normalizations(self) -> NormalizationsResource:
        return NormalizationsResource(self._client)

    @cached_property
    def prompts(self) -> PromptsResource:
        return PromptsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConfigurationsResourceWithRawResponse:
        return ConfigurationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigurationsResourceWithStreamingResponse:
        return ConfigurationsResourceWithStreamingResponse(self)


class AsyncConfigurationsResource(AsyncAPIResource):
    @cached_property
    def normalizations(self) -> AsyncNormalizationsResource:
        return AsyncNormalizationsResource(self._client)

    @cached_property
    def prompts(self) -> AsyncPromptsResource:
        return AsyncPromptsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConfigurationsResourceWithRawResponse:
        return AsyncConfigurationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigurationsResourceWithStreamingResponse:
        return AsyncConfigurationsResourceWithStreamingResponse(self)


class ConfigurationsResourceWithRawResponse:
    def __init__(self, configurations: ConfigurationsResource) -> None:
        self._configurations = configurations

    @cached_property
    def normalizations(self) -> NormalizationsResourceWithRawResponse:
        return NormalizationsResourceWithRawResponse(self._configurations.normalizations)

    @cached_property
    def prompts(self) -> PromptsResourceWithRawResponse:
        return PromptsResourceWithRawResponse(self._configurations.prompts)


class AsyncConfigurationsResourceWithRawResponse:
    def __init__(self, configurations: AsyncConfigurationsResource) -> None:
        self._configurations = configurations

    @cached_property
    def normalizations(self) -> AsyncNormalizationsResourceWithRawResponse:
        return AsyncNormalizationsResourceWithRawResponse(self._configurations.normalizations)

    @cached_property
    def prompts(self) -> AsyncPromptsResourceWithRawResponse:
        return AsyncPromptsResourceWithRawResponse(self._configurations.prompts)


class ConfigurationsResourceWithStreamingResponse:
    def __init__(self, configurations: ConfigurationsResource) -> None:
        self._configurations = configurations

    @cached_property
    def normalizations(self) -> NormalizationsResourceWithStreamingResponse:
        return NormalizationsResourceWithStreamingResponse(self._configurations.normalizations)

    @cached_property
    def prompts(self) -> PromptsResourceWithStreamingResponse:
        return PromptsResourceWithStreamingResponse(self._configurations.prompts)


class AsyncConfigurationsResourceWithStreamingResponse:
    def __init__(self, configurations: AsyncConfigurationsResource) -> None:
        self._configurations = configurations

    @cached_property
    def normalizations(self) -> AsyncNormalizationsResourceWithStreamingResponse:
        return AsyncNormalizationsResourceWithStreamingResponse(self._configurations.normalizations)

    @cached_property
    def prompts(self) -> AsyncPromptsResourceWithStreamingResponse:
        return AsyncPromptsResourceWithStreamingResponse(self._configurations.prompts)
