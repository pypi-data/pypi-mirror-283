# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
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
from ...types.configuration import normalization_create_params, normalization_update_params
from ...types.configuration.normalization_list_response import NormalizationListResponse
from ...types.configuration.normalization_create_response import NormalizationCreateResponse
from ...types.configuration.normalization_update_response import NormalizationUpdateResponse
from ...types.configuration.normalization_retrieve_response import NormalizationRetrieveResponse

__all__ = ["NormalizationsResource", "AsyncNormalizationsResource"]


class NormalizationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NormalizationsResourceWithRawResponse:
        return NormalizationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NormalizationsResourceWithStreamingResponse:
        return NormalizationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        created_by: str,
        name: str,
        normalization_type: str,
        output_data_source: str,
        output_filename: str,
        additional_params: Dict[str, Optional[str]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NormalizationCreateResponse:
        """
        Add Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/configuration/normalizations/normalizations",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "name": name,
                    "normalization_type": normalization_type,
                    "output_data_source": output_data_source,
                    "output_filename": output_filename,
                    "additional_params": additional_params,
                    "created_at": created_at,
                    "description": description,
                    "updated_at": updated_at,
                },
                normalization_create_params.NormalizationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationCreateResponse,
        )

    def retrieve(
        self,
        normalization_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NormalizationRetrieveResponse:
        """
        Get Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not normalization_id:
            raise ValueError(f"Expected a non-empty value for `normalization_id` but received {normalization_id!r}")
        return self._get(
            f"/configuration/normalizations/normalizations/{normalization_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationRetrieveResponse,
        )

    def update(
        self,
        normalization_id: str,
        *,
        created_by: str,
        name: str,
        normalization_type: str,
        output_data_source: str,
        output_filename: str,
        additional_params: Dict[str, Optional[str]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NormalizationUpdateResponse:
        """
        Update Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not normalization_id:
            raise ValueError(f"Expected a non-empty value for `normalization_id` but received {normalization_id!r}")
        return self._put(
            f"/configuration/normalizations/normalizations/{normalization_id}",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "name": name,
                    "normalization_type": normalization_type,
                    "output_data_source": output_data_source,
                    "output_filename": output_filename,
                    "additional_params": additional_params,
                    "created_at": created_at,
                    "description": description,
                    "updated_at": updated_at,
                },
                normalization_update_params.NormalizationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationUpdateResponse,
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
    ) -> NormalizationListResponse:
        """List Normalizations"""
        return self._get(
            "/configuration/normalizations/normalizations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationListResponse,
        )

    def delete(
        self,
        normalization_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not normalization_id:
            raise ValueError(f"Expected a non-empty value for `normalization_id` but received {normalization_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/configuration/normalizations/normalizations/{normalization_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncNormalizationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNormalizationsResourceWithRawResponse:
        return AsyncNormalizationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNormalizationsResourceWithStreamingResponse:
        return AsyncNormalizationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        created_by: str,
        name: str,
        normalization_type: str,
        output_data_source: str,
        output_filename: str,
        additional_params: Dict[str, Optional[str]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NormalizationCreateResponse:
        """
        Add Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/configuration/normalizations/normalizations",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "name": name,
                    "normalization_type": normalization_type,
                    "output_data_source": output_data_source,
                    "output_filename": output_filename,
                    "additional_params": additional_params,
                    "created_at": created_at,
                    "description": description,
                    "updated_at": updated_at,
                },
                normalization_create_params.NormalizationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationCreateResponse,
        )

    async def retrieve(
        self,
        normalization_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NormalizationRetrieveResponse:
        """
        Get Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not normalization_id:
            raise ValueError(f"Expected a non-empty value for `normalization_id` but received {normalization_id!r}")
        return await self._get(
            f"/configuration/normalizations/normalizations/{normalization_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationRetrieveResponse,
        )

    async def update(
        self,
        normalization_id: str,
        *,
        created_by: str,
        name: str,
        normalization_type: str,
        output_data_source: str,
        output_filename: str,
        additional_params: Dict[str, Optional[str]] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NormalizationUpdateResponse:
        """
        Update Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not normalization_id:
            raise ValueError(f"Expected a non-empty value for `normalization_id` but received {normalization_id!r}")
        return await self._put(
            f"/configuration/normalizations/normalizations/{normalization_id}",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "name": name,
                    "normalization_type": normalization_type,
                    "output_data_source": output_data_source,
                    "output_filename": output_filename,
                    "additional_params": additional_params,
                    "created_at": created_at,
                    "description": description,
                    "updated_at": updated_at,
                },
                normalization_update_params.NormalizationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationUpdateResponse,
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
    ) -> NormalizationListResponse:
        """List Normalizations"""
        return await self._get(
            "/configuration/normalizations/normalizations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NormalizationListResponse,
        )

    async def delete(
        self,
        normalization_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Normalization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not normalization_id:
            raise ValueError(f"Expected a non-empty value for `normalization_id` but received {normalization_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/configuration/normalizations/normalizations/{normalization_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class NormalizationsResourceWithRawResponse:
    def __init__(self, normalizations: NormalizationsResource) -> None:
        self._normalizations = normalizations

        self.create = to_raw_response_wrapper(
            normalizations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            normalizations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            normalizations.update,
        )
        self.list = to_raw_response_wrapper(
            normalizations.list,
        )
        self.delete = to_raw_response_wrapper(
            normalizations.delete,
        )


class AsyncNormalizationsResourceWithRawResponse:
    def __init__(self, normalizations: AsyncNormalizationsResource) -> None:
        self._normalizations = normalizations

        self.create = async_to_raw_response_wrapper(
            normalizations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            normalizations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            normalizations.update,
        )
        self.list = async_to_raw_response_wrapper(
            normalizations.list,
        )
        self.delete = async_to_raw_response_wrapper(
            normalizations.delete,
        )


class NormalizationsResourceWithStreamingResponse:
    def __init__(self, normalizations: NormalizationsResource) -> None:
        self._normalizations = normalizations

        self.create = to_streamed_response_wrapper(
            normalizations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            normalizations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            normalizations.update,
        )
        self.list = to_streamed_response_wrapper(
            normalizations.list,
        )
        self.delete = to_streamed_response_wrapper(
            normalizations.delete,
        )


class AsyncNormalizationsResourceWithStreamingResponse:
    def __init__(self, normalizations: AsyncNormalizationsResource) -> None:
        self._normalizations = normalizations

        self.create = async_to_streamed_response_wrapper(
            normalizations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            normalizations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            normalizations.update,
        )
        self.list = async_to_streamed_response_wrapper(
            normalizations.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            normalizations.delete,
        )
