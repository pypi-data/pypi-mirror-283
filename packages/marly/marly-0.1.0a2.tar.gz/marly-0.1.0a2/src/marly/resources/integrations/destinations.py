# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ...types.integrations import destination_register_s3_params, destination_register_excel_params
from ...types.integrations.destination_register_s3_response import DestinationRegisterS3Response
from ...types.integrations.destination_register_excel_response import DestinationRegisterExcelResponse

__all__ = ["DestinationsResource", "AsyncDestinationsResource"]


class DestinationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DestinationsResourceWithRawResponse:
        return DestinationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DestinationsResourceWithStreamingResponse:
        return DestinationsResourceWithStreamingResponse(self)

    def register_excel(
        self,
        *,
        data_source: str,
        output_filename: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationRegisterExcelResponse:
        """
        Register Excel Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/integrations/destinations/register_excel",
            body=maybe_transform(
                {
                    "data_source": data_source,
                    "output_filename": output_filename,
                },
                destination_register_excel_params.DestinationRegisterExcelParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationRegisterExcelResponse,
        )

    def register_s3(
        self,
        *,
        aws_access_key: str,
        aws_secret_key: str,
        bucket_name: str,
        region_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationRegisterS3Response:
        """
        Register S3 Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/integrations/destinations/register_s3",
            body=maybe_transform(
                {
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "bucket_name": bucket_name,
                    "region_name": region_name,
                },
                destination_register_s3_params.DestinationRegisterS3Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationRegisterS3Response,
        )


class AsyncDestinationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDestinationsResourceWithRawResponse:
        return AsyncDestinationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDestinationsResourceWithStreamingResponse:
        return AsyncDestinationsResourceWithStreamingResponse(self)

    async def register_excel(
        self,
        *,
        data_source: str,
        output_filename: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationRegisterExcelResponse:
        """
        Register Excel Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/integrations/destinations/register_excel",
            body=await async_maybe_transform(
                {
                    "data_source": data_source,
                    "output_filename": output_filename,
                },
                destination_register_excel_params.DestinationRegisterExcelParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationRegisterExcelResponse,
        )

    async def register_s3(
        self,
        *,
        aws_access_key: str,
        aws_secret_key: str,
        bucket_name: str,
        region_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationRegisterS3Response:
        """
        Register S3 Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/integrations/destinations/register_s3",
            body=await async_maybe_transform(
                {
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "bucket_name": bucket_name,
                    "region_name": region_name,
                },
                destination_register_s3_params.DestinationRegisterS3Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationRegisterS3Response,
        )


class DestinationsResourceWithRawResponse:
    def __init__(self, destinations: DestinationsResource) -> None:
        self._destinations = destinations

        self.register_excel = to_raw_response_wrapper(
            destinations.register_excel,
        )
        self.register_s3 = to_raw_response_wrapper(
            destinations.register_s3,
        )


class AsyncDestinationsResourceWithRawResponse:
    def __init__(self, destinations: AsyncDestinationsResource) -> None:
        self._destinations = destinations

        self.register_excel = async_to_raw_response_wrapper(
            destinations.register_excel,
        )
        self.register_s3 = async_to_raw_response_wrapper(
            destinations.register_s3,
        )


class DestinationsResourceWithStreamingResponse:
    def __init__(self, destinations: DestinationsResource) -> None:
        self._destinations = destinations

        self.register_excel = to_streamed_response_wrapper(
            destinations.register_excel,
        )
        self.register_s3 = to_streamed_response_wrapper(
            destinations.register_s3,
        )


class AsyncDestinationsResourceWithStreamingResponse:
    def __init__(self, destinations: AsyncDestinationsResource) -> None:
        self._destinations = destinations

        self.register_excel = async_to_streamed_response_wrapper(
            destinations.register_excel,
        )
        self.register_s3 = async_to_streamed_response_wrapper(
            destinations.register_s3,
        )
