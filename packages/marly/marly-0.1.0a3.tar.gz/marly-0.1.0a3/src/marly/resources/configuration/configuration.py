# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .models import (
    ModelsResource,
    AsyncModelsResource,
    ModelsResourceWithRawResponse,
    AsyncModelsResourceWithRawResponse,
    ModelsResourceWithStreamingResponse,
    AsyncModelsResourceWithStreamingResponse,
)
from .prompts import (
    PromptsResource,
    AsyncPromptsResource,
    PromptsResourceWithRawResponse,
    AsyncPromptsResourceWithRawResponse,
    PromptsResourceWithStreamingResponse,
    AsyncPromptsResourceWithStreamingResponse,
)
from .schemas import (
    SchemasResource,
    AsyncSchemasResource,
    SchemasResourceWithRawResponse,
    AsyncSchemasResourceWithRawResponse,
    SchemasResourceWithStreamingResponse,
    AsyncSchemasResourceWithStreamingResponse,
)
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
from .normalizations import (
    NormalizationsResource,
    AsyncNormalizationsResource,
    NormalizationsResourceWithRawResponse,
    AsyncNormalizationsResourceWithRawResponse,
    NormalizationsResourceWithStreamingResponse,
    AsyncNormalizationsResourceWithStreamingResponse,
)
from .output_mappings import (
    OutputMappingsResource,
    AsyncOutputMappingsResource,
    OutputMappingsResourceWithRawResponse,
    AsyncOutputMappingsResourceWithRawResponse,
    OutputMappingsResourceWithStreamingResponse,
    AsyncOutputMappingsResourceWithStreamingResponse,
)

__all__ = ["ConfigurationResource", "AsyncConfigurationResource"]


class ConfigurationResource(SyncAPIResource):
    @cached_property
    def models(self) -> ModelsResource:
        return ModelsResource(self._client)

    @cached_property
    def schemas(self) -> SchemasResource:
        return SchemasResource(self._client)

    @cached_property
    def pipelines(self) -> PipelinesResource:
        return PipelinesResource(self._client)

    @cached_property
    def output_mappings(self) -> OutputMappingsResource:
        return OutputMappingsResource(self._client)

    @cached_property
    def normalizations(self) -> NormalizationsResource:
        return NormalizationsResource(self._client)

    @cached_property
    def prompts(self) -> PromptsResource:
        return PromptsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConfigurationResourceWithRawResponse:
        return ConfigurationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigurationResourceWithStreamingResponse:
        return ConfigurationResourceWithStreamingResponse(self)


class AsyncConfigurationResource(AsyncAPIResource):
    @cached_property
    def models(self) -> AsyncModelsResource:
        return AsyncModelsResource(self._client)

    @cached_property
    def schemas(self) -> AsyncSchemasResource:
        return AsyncSchemasResource(self._client)

    @cached_property
    def pipelines(self) -> AsyncPipelinesResource:
        return AsyncPipelinesResource(self._client)

    @cached_property
    def output_mappings(self) -> AsyncOutputMappingsResource:
        return AsyncOutputMappingsResource(self._client)

    @cached_property
    def normalizations(self) -> AsyncNormalizationsResource:
        return AsyncNormalizationsResource(self._client)

    @cached_property
    def prompts(self) -> AsyncPromptsResource:
        return AsyncPromptsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConfigurationResourceWithRawResponse:
        return AsyncConfigurationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigurationResourceWithStreamingResponse:
        return AsyncConfigurationResourceWithStreamingResponse(self)


class ConfigurationResourceWithRawResponse:
    def __init__(self, configuration: ConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def models(self) -> ModelsResourceWithRawResponse:
        return ModelsResourceWithRawResponse(self._configuration.models)

    @cached_property
    def schemas(self) -> SchemasResourceWithRawResponse:
        return SchemasResourceWithRawResponse(self._configuration.schemas)

    @cached_property
    def pipelines(self) -> PipelinesResourceWithRawResponse:
        return PipelinesResourceWithRawResponse(self._configuration.pipelines)

    @cached_property
    def output_mappings(self) -> OutputMappingsResourceWithRawResponse:
        return OutputMappingsResourceWithRawResponse(self._configuration.output_mappings)

    @cached_property
    def normalizations(self) -> NormalizationsResourceWithRawResponse:
        return NormalizationsResourceWithRawResponse(self._configuration.normalizations)

    @cached_property
    def prompts(self) -> PromptsResourceWithRawResponse:
        return PromptsResourceWithRawResponse(self._configuration.prompts)


class AsyncConfigurationResourceWithRawResponse:
    def __init__(self, configuration: AsyncConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def models(self) -> AsyncModelsResourceWithRawResponse:
        return AsyncModelsResourceWithRawResponse(self._configuration.models)

    @cached_property
    def schemas(self) -> AsyncSchemasResourceWithRawResponse:
        return AsyncSchemasResourceWithRawResponse(self._configuration.schemas)

    @cached_property
    def pipelines(self) -> AsyncPipelinesResourceWithRawResponse:
        return AsyncPipelinesResourceWithRawResponse(self._configuration.pipelines)

    @cached_property
    def output_mappings(self) -> AsyncOutputMappingsResourceWithRawResponse:
        return AsyncOutputMappingsResourceWithRawResponse(self._configuration.output_mappings)

    @cached_property
    def normalizations(self) -> AsyncNormalizationsResourceWithRawResponse:
        return AsyncNormalizationsResourceWithRawResponse(self._configuration.normalizations)

    @cached_property
    def prompts(self) -> AsyncPromptsResourceWithRawResponse:
        return AsyncPromptsResourceWithRawResponse(self._configuration.prompts)


class ConfigurationResourceWithStreamingResponse:
    def __init__(self, configuration: ConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def models(self) -> ModelsResourceWithStreamingResponse:
        return ModelsResourceWithStreamingResponse(self._configuration.models)

    @cached_property
    def schemas(self) -> SchemasResourceWithStreamingResponse:
        return SchemasResourceWithStreamingResponse(self._configuration.schemas)

    @cached_property
    def pipelines(self) -> PipelinesResourceWithStreamingResponse:
        return PipelinesResourceWithStreamingResponse(self._configuration.pipelines)

    @cached_property
    def output_mappings(self) -> OutputMappingsResourceWithStreamingResponse:
        return OutputMappingsResourceWithStreamingResponse(self._configuration.output_mappings)

    @cached_property
    def normalizations(self) -> NormalizationsResourceWithStreamingResponse:
        return NormalizationsResourceWithStreamingResponse(self._configuration.normalizations)

    @cached_property
    def prompts(self) -> PromptsResourceWithStreamingResponse:
        return PromptsResourceWithStreamingResponse(self._configuration.prompts)


class AsyncConfigurationResourceWithStreamingResponse:
    def __init__(self, configuration: AsyncConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def models(self) -> AsyncModelsResourceWithStreamingResponse:
        return AsyncModelsResourceWithStreamingResponse(self._configuration.models)

    @cached_property
    def schemas(self) -> AsyncSchemasResourceWithStreamingResponse:
        return AsyncSchemasResourceWithStreamingResponse(self._configuration.schemas)

    @cached_property
    def pipelines(self) -> AsyncPipelinesResourceWithStreamingResponse:
        return AsyncPipelinesResourceWithStreamingResponse(self._configuration.pipelines)

    @cached_property
    def output_mappings(self) -> AsyncOutputMappingsResourceWithStreamingResponse:
        return AsyncOutputMappingsResourceWithStreamingResponse(self._configuration.output_mappings)

    @cached_property
    def normalizations(self) -> AsyncNormalizationsResourceWithStreamingResponse:
        return AsyncNormalizationsResourceWithStreamingResponse(self._configuration.normalizations)

    @cached_property
    def prompts(self) -> AsyncPromptsResourceWithStreamingResponse:
        return AsyncPromptsResourceWithStreamingResponse(self._configuration.prompts)
