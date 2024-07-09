# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import (
    make_request_options,
)
from ...types.configuration import pipeline_create_params, pipeline_update_params
from ...types.configuration.pipeline_list_response import PipelineListResponse
from ...types.configuration.pipeline_create_response import PipelineCreateResponse
from ...types.configuration.pipeline_update_response import PipelineUpdateResponse
from ...types.configuration.pipeline_retrieve_response import PipelineRetrieveResponse

__all__ = ["PipelinesResource", "AsyncPipelinesResource"]


class PipelinesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PipelinesResourceWithRawResponse:
        return PipelinesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PipelinesResourceWithStreamingResponse:
        return PipelinesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        created_by: str,
        model_id: str,
        name: str,
        pipeline_schema_id: str,
        run_type: str,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        integrations: Dict[str, str] | NotGiven = NOT_GIVEN,
        normalization_id: str | NotGiven = NOT_GIVEN,
        prompt_ids: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineCreateResponse:
        """
        Add Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/configuration/pipelines/pipelines",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "model_id": model_id,
                    "name": name,
                    "pipeline_schema_id": pipeline_schema_id,
                    "run_type": run_type,
                    "created_at": created_at,
                    "integrations": integrations,
                    "normalization_id": normalization_id,
                    "prompt_ids": prompt_ids,
                    "status": status,
                    "updated_at": updated_at,
                },
                pipeline_create_params.PipelineCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineCreateResponse,
        )

    def retrieve(
        self,
        pipeline_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineRetrieveResponse:
        """
        Get Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        return self._get(
            f"/configuration/pipelines/pipelines/{pipeline_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineRetrieveResponse,
        )

    def update(
        self,
        pipeline_id: str,
        *,
        created_by: str,
        model_id: str,
        name: str,
        pipeline_schema_id: str,
        run_type: str,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        integrations: Dict[str, str] | NotGiven = NOT_GIVEN,
        normalization_id: str | NotGiven = NOT_GIVEN,
        prompt_ids: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineUpdateResponse:
        """
        Update Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        return self._put(
            f"/configuration/pipelines/pipelines/{pipeline_id}",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "model_id": model_id,
                    "name": name,
                    "pipeline_schema_id": pipeline_schema_id,
                    "run_type": run_type,
                    "created_at": created_at,
                    "integrations": integrations,
                    "normalization_id": normalization_id,
                    "prompt_ids": prompt_ids,
                    "status": status,
                    "updated_at": updated_at,
                },
                pipeline_update_params.PipelineUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineUpdateResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineListResponse:
        """List Pipelines"""
        return self._get(
            "/configuration/pipelines/pipelines",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineListResponse,
        )

    def delete(
        self,
        pipeline_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/configuration/pipelines/pipelines/{pipeline_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncPipelinesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPipelinesResourceWithRawResponse:
        return AsyncPipelinesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPipelinesResourceWithStreamingResponse:
        return AsyncPipelinesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        created_by: str,
        model_id: str,
        name: str,
        pipeline_schema_id: str,
        run_type: str,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        integrations: Dict[str, str] | NotGiven = NOT_GIVEN,
        normalization_id: str | NotGiven = NOT_GIVEN,
        prompt_ids: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineCreateResponse:
        """
        Add Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/configuration/pipelines/pipelines",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "model_id": model_id,
                    "name": name,
                    "pipeline_schema_id": pipeline_schema_id,
                    "run_type": run_type,
                    "created_at": created_at,
                    "integrations": integrations,
                    "normalization_id": normalization_id,
                    "prompt_ids": prompt_ids,
                    "status": status,
                    "updated_at": updated_at,
                },
                pipeline_create_params.PipelineCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineCreateResponse,
        )

    async def retrieve(
        self,
        pipeline_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineRetrieveResponse:
        """
        Get Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        return await self._get(
            f"/configuration/pipelines/pipelines/{pipeline_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineRetrieveResponse,
        )

    async def update(
        self,
        pipeline_id: str,
        *,
        created_by: str,
        model_id: str,
        name: str,
        pipeline_schema_id: str,
        run_type: str,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        integrations: Dict[str, str] | NotGiven = NOT_GIVEN,
        normalization_id: str | NotGiven = NOT_GIVEN,
        prompt_ids: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineUpdateResponse:
        """
        Update Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        return await self._put(
            f"/configuration/pipelines/pipelines/{pipeline_id}",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "model_id": model_id,
                    "name": name,
                    "pipeline_schema_id": pipeline_schema_id,
                    "run_type": run_type,
                    "created_at": created_at,
                    "integrations": integrations,
                    "normalization_id": normalization_id,
                    "prompt_ids": prompt_ids,
                    "status": status,
                    "updated_at": updated_at,
                },
                pipeline_update_params.PipelineUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineUpdateResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineListResponse:
        """List Pipelines"""
        return await self._get(
            "/configuration/pipelines/pipelines",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineListResponse,
        )

    async def delete(
        self,
        pipeline_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Pipeline

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/configuration/pipelines/pipelines/{pipeline_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class PipelinesResourceWithRawResponse:
    def __init__(self, pipelines: PipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = to_raw_response_wrapper(
            pipelines.create,
        )
        self.retrieve = to_raw_response_wrapper(
            pipelines.retrieve,
        )
        self.update = to_raw_response_wrapper(
            pipelines.update,
        )
        self.list = to_raw_response_wrapper(
            pipelines.list,
        )
        self.delete = to_raw_response_wrapper(
            pipelines.delete,
        )


class AsyncPipelinesResourceWithRawResponse:
    def __init__(self, pipelines: AsyncPipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = async_to_raw_response_wrapper(
            pipelines.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            pipelines.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            pipelines.update,
        )
        self.list = async_to_raw_response_wrapper(
            pipelines.list,
        )
        self.delete = async_to_raw_response_wrapper(
            pipelines.delete,
        )


class PipelinesResourceWithStreamingResponse:
    def __init__(self, pipelines: PipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = to_streamed_response_wrapper(
            pipelines.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            pipelines.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            pipelines.update,
        )
        self.list = to_streamed_response_wrapper(
            pipelines.list,
        )
        self.delete = to_streamed_response_wrapper(
            pipelines.delete,
        )


class AsyncPipelinesResourceWithStreamingResponse:
    def __init__(self, pipelines: AsyncPipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = async_to_streamed_response_wrapper(
            pipelines.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            pipelines.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            pipelines.update,
        )
        self.list = async_to_streamed_response_wrapper(
            pipelines.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            pipelines.delete,
        )
