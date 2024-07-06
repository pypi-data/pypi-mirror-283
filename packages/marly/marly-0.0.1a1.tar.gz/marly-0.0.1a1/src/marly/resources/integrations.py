# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import integration_register_s3_params, integration_register_excel_params
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
from ..types.register_integration_response import RegisterIntegrationResponse

__all__ = ["IntegrationsResource", "AsyncIntegrationsResource"]


class IntegrationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> IntegrationsResourceWithRawResponse:
        return IntegrationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IntegrationsResourceWithStreamingResponse:
        return IntegrationsResourceWithStreamingResponse(self)

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
    ) -> RegisterIntegrationResponse:
        """
        Register Excel Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/integrations/register_excel",
            body=maybe_transform(
                {
                    "data_source": data_source,
                    "output_filename": output_filename,
                },
                integration_register_excel_params.IntegrationRegisterExcelParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RegisterIntegrationResponse,
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
    ) -> RegisterIntegrationResponse:
        """
        Register S3 Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/integrations/register_s3",
            body=maybe_transform(
                {
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "bucket_name": bucket_name,
                    "region_name": region_name,
                },
                integration_register_s3_params.IntegrationRegisterS3Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RegisterIntegrationResponse,
        )


class AsyncIntegrationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncIntegrationsResourceWithRawResponse:
        return AsyncIntegrationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIntegrationsResourceWithStreamingResponse:
        return AsyncIntegrationsResourceWithStreamingResponse(self)

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
    ) -> RegisterIntegrationResponse:
        """
        Register Excel Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/integrations/register_excel",
            body=await async_maybe_transform(
                {
                    "data_source": data_source,
                    "output_filename": output_filename,
                },
                integration_register_excel_params.IntegrationRegisterExcelParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RegisterIntegrationResponse,
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
    ) -> RegisterIntegrationResponse:
        """
        Register S3 Destination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/integrations/register_s3",
            body=await async_maybe_transform(
                {
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "bucket_name": bucket_name,
                    "region_name": region_name,
                },
                integration_register_s3_params.IntegrationRegisterS3Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RegisterIntegrationResponse,
        )


class IntegrationsResourceWithRawResponse:
    def __init__(self, integrations: IntegrationsResource) -> None:
        self._integrations = integrations

        self.register_excel = to_raw_response_wrapper(
            integrations.register_excel,
        )
        self.register_s3 = to_raw_response_wrapper(
            integrations.register_s3,
        )


class AsyncIntegrationsResourceWithRawResponse:
    def __init__(self, integrations: AsyncIntegrationsResource) -> None:
        self._integrations = integrations

        self.register_excel = async_to_raw_response_wrapper(
            integrations.register_excel,
        )
        self.register_s3 = async_to_raw_response_wrapper(
            integrations.register_s3,
        )


class IntegrationsResourceWithStreamingResponse:
    def __init__(self, integrations: IntegrationsResource) -> None:
        self._integrations = integrations

        self.register_excel = to_streamed_response_wrapper(
            integrations.register_excel,
        )
        self.register_s3 = to_streamed_response_wrapper(
            integrations.register_s3,
        )


class AsyncIntegrationsResourceWithStreamingResponse:
    def __init__(self, integrations: AsyncIntegrationsResource) -> None:
        self._integrations = integrations

        self.register_excel = async_to_streamed_response_wrapper(
            integrations.register_excel,
        )
        self.register_s3 = async_to_streamed_response_wrapper(
            integrations.register_s3,
        )
