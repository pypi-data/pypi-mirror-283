# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
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
from ...types.configuration import output_mapping_create_params, output_mapping_update_params
from ...types.configuration.output_mapping_list_response import OutputMappingListResponse
from ...types.configuration.output_mapping_create_response import OutputMappingCreateResponse
from ...types.configuration.output_mapping_update_response import OutputMappingUpdateResponse
from ...types.configuration.output_mapping_retrieve_response import OutputMappingRetrieveResponse

__all__ = ["OutputMappingsResource", "AsyncOutputMappingsResource"]


class OutputMappingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OutputMappingsResourceWithRawResponse:
        return OutputMappingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OutputMappingsResourceWithStreamingResponse:
        return OutputMappingsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        created_by: str,
        column_locations: Optional[Dict[str, Dict[str, str]]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        data_locations: List[str] | NotGiven = NOT_GIVEN,
        output_data_type: Optional[str] | NotGiven = NOT_GIVEN,
        output_filename: Optional[str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutputMappingCreateResponse:
        """
        Add Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/configuration/output-mappings/output-mappings",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "column_locations": column_locations,
                    "created_at": created_at,
                    "data_locations": data_locations,
                    "output_data_type": output_data_type,
                    "output_filename": output_filename,
                    "status": status,
                    "updated_at": updated_at,
                },
                output_mapping_create_params.OutputMappingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingCreateResponse,
        )

    def retrieve(
        self,
        output_mapping_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutputMappingRetrieveResponse:
        """
        Get Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not output_mapping_id:
            raise ValueError(f"Expected a non-empty value for `output_mapping_id` but received {output_mapping_id!r}")
        return self._get(
            f"/configuration/output-mappings/output-mappings/{output_mapping_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingRetrieveResponse,
        )

    def update(
        self,
        output_mapping_id: str,
        *,
        created_by: str,
        column_locations: Optional[Dict[str, Dict[str, str]]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        data_locations: List[str] | NotGiven = NOT_GIVEN,
        output_data_type: Optional[str] | NotGiven = NOT_GIVEN,
        output_filename: Optional[str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutputMappingUpdateResponse:
        """
        Update Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not output_mapping_id:
            raise ValueError(f"Expected a non-empty value for `output_mapping_id` but received {output_mapping_id!r}")
        return self._put(
            f"/configuration/output-mappings/output-mappings/{output_mapping_id}",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "column_locations": column_locations,
                    "created_at": created_at,
                    "data_locations": data_locations,
                    "output_data_type": output_data_type,
                    "output_filename": output_filename,
                    "status": status,
                    "updated_at": updated_at,
                },
                output_mapping_update_params.OutputMappingUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingUpdateResponse,
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
    ) -> OutputMappingListResponse:
        """List Output Mappings"""
        return self._get(
            "/configuration/output-mappings/output-mappings",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingListResponse,
        )

    def delete(
        self,
        output_mapping_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not output_mapping_id:
            raise ValueError(f"Expected a non-empty value for `output_mapping_id` but received {output_mapping_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/configuration/output-mappings/output-mappings/{output_mapping_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncOutputMappingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOutputMappingsResourceWithRawResponse:
        return AsyncOutputMappingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOutputMappingsResourceWithStreamingResponse:
        return AsyncOutputMappingsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        created_by: str,
        column_locations: Optional[Dict[str, Dict[str, str]]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        data_locations: List[str] | NotGiven = NOT_GIVEN,
        output_data_type: Optional[str] | NotGiven = NOT_GIVEN,
        output_filename: Optional[str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutputMappingCreateResponse:
        """
        Add Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/configuration/output-mappings/output-mappings",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "column_locations": column_locations,
                    "created_at": created_at,
                    "data_locations": data_locations,
                    "output_data_type": output_data_type,
                    "output_filename": output_filename,
                    "status": status,
                    "updated_at": updated_at,
                },
                output_mapping_create_params.OutputMappingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingCreateResponse,
        )

    async def retrieve(
        self,
        output_mapping_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutputMappingRetrieveResponse:
        """
        Get Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not output_mapping_id:
            raise ValueError(f"Expected a non-empty value for `output_mapping_id` but received {output_mapping_id!r}")
        return await self._get(
            f"/configuration/output-mappings/output-mappings/{output_mapping_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingRetrieveResponse,
        )

    async def update(
        self,
        output_mapping_id: str,
        *,
        created_by: str,
        column_locations: Optional[Dict[str, Dict[str, str]]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        data_locations: List[str] | NotGiven = NOT_GIVEN,
        output_data_type: Optional[str] | NotGiven = NOT_GIVEN,
        output_filename: Optional[str] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutputMappingUpdateResponse:
        """
        Update Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not output_mapping_id:
            raise ValueError(f"Expected a non-empty value for `output_mapping_id` but received {output_mapping_id!r}")
        return await self._put(
            f"/configuration/output-mappings/output-mappings/{output_mapping_id}",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "column_locations": column_locations,
                    "created_at": created_at,
                    "data_locations": data_locations,
                    "output_data_type": output_data_type,
                    "output_filename": output_filename,
                    "status": status,
                    "updated_at": updated_at,
                },
                output_mapping_update_params.OutputMappingUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingUpdateResponse,
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
    ) -> OutputMappingListResponse:
        """List Output Mappings"""
        return await self._get(
            "/configuration/output-mappings/output-mappings",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutputMappingListResponse,
        )

    async def delete(
        self,
        output_mapping_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Output Mapping

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not output_mapping_id:
            raise ValueError(f"Expected a non-empty value for `output_mapping_id` but received {output_mapping_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/configuration/output-mappings/output-mappings/{output_mapping_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class OutputMappingsResourceWithRawResponse:
    def __init__(self, output_mappings: OutputMappingsResource) -> None:
        self._output_mappings = output_mappings

        self.create = to_raw_response_wrapper(
            output_mappings.create,
        )
        self.retrieve = to_raw_response_wrapper(
            output_mappings.retrieve,
        )
        self.update = to_raw_response_wrapper(
            output_mappings.update,
        )
        self.list = to_raw_response_wrapper(
            output_mappings.list,
        )
        self.delete = to_raw_response_wrapper(
            output_mappings.delete,
        )


class AsyncOutputMappingsResourceWithRawResponse:
    def __init__(self, output_mappings: AsyncOutputMappingsResource) -> None:
        self._output_mappings = output_mappings

        self.create = async_to_raw_response_wrapper(
            output_mappings.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            output_mappings.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            output_mappings.update,
        )
        self.list = async_to_raw_response_wrapper(
            output_mappings.list,
        )
        self.delete = async_to_raw_response_wrapper(
            output_mappings.delete,
        )


class OutputMappingsResourceWithStreamingResponse:
    def __init__(self, output_mappings: OutputMappingsResource) -> None:
        self._output_mappings = output_mappings

        self.create = to_streamed_response_wrapper(
            output_mappings.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            output_mappings.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            output_mappings.update,
        )
        self.list = to_streamed_response_wrapper(
            output_mappings.list,
        )
        self.delete = to_streamed_response_wrapper(
            output_mappings.delete,
        )


class AsyncOutputMappingsResourceWithStreamingResponse:
    def __init__(self, output_mappings: AsyncOutputMappingsResource) -> None:
        self._output_mappings = output_mappings

        self.create = async_to_streamed_response_wrapper(
            output_mappings.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            output_mappings.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            output_mappings.update,
        )
        self.list = async_to_streamed_response_wrapper(
            output_mappings.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            output_mappings.delete,
        )
