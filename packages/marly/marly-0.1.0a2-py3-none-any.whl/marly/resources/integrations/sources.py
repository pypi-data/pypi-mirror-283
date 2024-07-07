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
from ...types.integrations import source_register_s3_params
from ...types.integrations.source_register_s3_response import SourceRegisterS3Response

__all__ = ["SourcesResource", "AsyncSourcesResource"]


class SourcesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SourcesResourceWithRawResponse:
        return SourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SourcesResourceWithStreamingResponse:
        return SourcesResourceWithStreamingResponse(self)

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
    ) -> SourceRegisterS3Response:
        """
        Register S3 Integration

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/integrations/sources/register-s3",
            body=maybe_transform(
                {
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "bucket_name": bucket_name,
                    "region_name": region_name,
                },
                source_register_s3_params.SourceRegisterS3Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SourceRegisterS3Response,
        )


class AsyncSourcesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSourcesResourceWithRawResponse:
        return AsyncSourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSourcesResourceWithStreamingResponse:
        return AsyncSourcesResourceWithStreamingResponse(self)

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
    ) -> SourceRegisterS3Response:
        """
        Register S3 Integration

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/integrations/sources/register-s3",
            body=await async_maybe_transform(
                {
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "bucket_name": bucket_name,
                    "region_name": region_name,
                },
                source_register_s3_params.SourceRegisterS3Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SourceRegisterS3Response,
        )


class SourcesResourceWithRawResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.register_s3 = to_raw_response_wrapper(
            sources.register_s3,
        )


class AsyncSourcesResourceWithRawResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.register_s3 = async_to_raw_response_wrapper(
            sources.register_s3,
        )


class SourcesResourceWithStreamingResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.register_s3 = to_streamed_response_wrapper(
            sources.register_s3,
        )


class AsyncSourcesResourceWithStreamingResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.register_s3 = async_to_streamed_response_wrapper(
            sources.register_s3,
        )
