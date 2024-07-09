# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
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
from ...types.configuration import prompt_create_params, prompt_update_params
from ...types.configuration.prompt_list_response import PromptListResponse
from ...types.configuration.prompt_create_response import PromptCreateResponse
from ...types.configuration.prompt_update_response import PromptUpdateResponse
from ...types.configuration.prompt_retrieve_response import PromptRetrieveResponse

__all__ = ["PromptsResource", "AsyncPromptsResource"]


class PromptsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PromptsResourceWithRawResponse:
        return PromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PromptsResourceWithStreamingResponse:
        return PromptsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        created_by: str,
        messages: Iterable[prompt_create_params.Message],
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        response_format: str | NotGiven = NOT_GIVEN,
        type: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        variables: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateResponse:
        """
        Add Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/configuration/prompts/prompts",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "messages": messages,
                    "created_at": created_at,
                    "name": name,
                    "prompt_id": prompt_id,
                    "response_format": response_format,
                    "type": type,
                    "updated_at": updated_at,
                    "variables": variables,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateResponse,
        )

    def retrieve(
        self,
        prompt_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptRetrieveResponse:
        """
        Get Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not prompt_id:
            raise ValueError(f"Expected a non-empty value for `prompt_id` but received {prompt_id!r}")
        return self._get(
            f"/configuration/prompts/prompts/{prompt_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptRetrieveResponse,
        )

    def update(
        self,
        *,
        path_prompt_id: str,
        created_by: str,
        messages: Iterable[prompt_update_params.Message],
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        body_prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        response_format: str | NotGiven = NOT_GIVEN,
        type: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        variables: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptUpdateResponse:
        """
        Update Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_prompt_id:
            raise ValueError(f"Expected a non-empty value for `path_prompt_id` but received {path_prompt_id!r}")
        return self._put(
            f"/configuration/prompts/prompts/{path_prompt_id}",
            body=maybe_transform(
                {
                    "created_by": created_by,
                    "messages": messages,
                    "created_at": created_at,
                    "name": name,
                    "prompt_id": body_prompt_id,
                    "response_format": response_format,
                    "type": type,
                    "updated_at": updated_at,
                    "variables": variables,
                },
                prompt_update_params.PromptUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptUpdateResponse,
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
    ) -> PromptListResponse:
        """List Prompts"""
        return self._get(
            "/configuration/prompts/prompts",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptListResponse,
        )

    def delete(
        self,
        prompt_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not prompt_id:
            raise ValueError(f"Expected a non-empty value for `prompt_id` but received {prompt_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/configuration/prompts/prompts/{prompt_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncPromptsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPromptsResourceWithRawResponse:
        return AsyncPromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPromptsResourceWithStreamingResponse:
        return AsyncPromptsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        created_by: str,
        messages: Iterable[prompt_create_params.Message],
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        response_format: str | NotGiven = NOT_GIVEN,
        type: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        variables: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateResponse:
        """
        Add Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/configuration/prompts/prompts",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "messages": messages,
                    "created_at": created_at,
                    "name": name,
                    "prompt_id": prompt_id,
                    "response_format": response_format,
                    "type": type,
                    "updated_at": updated_at,
                    "variables": variables,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateResponse,
        )

    async def retrieve(
        self,
        prompt_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptRetrieveResponse:
        """
        Get Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not prompt_id:
            raise ValueError(f"Expected a non-empty value for `prompt_id` but received {prompt_id!r}")
        return await self._get(
            f"/configuration/prompts/prompts/{prompt_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptRetrieveResponse,
        )

    async def update(
        self,
        *,
        path_prompt_id: str,
        created_by: str,
        messages: Iterable[prompt_update_params.Message],
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        body_prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        response_format: str | NotGiven = NOT_GIVEN,
        type: Optional[str] | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        variables: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptUpdateResponse:
        """
        Update Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_prompt_id:
            raise ValueError(f"Expected a non-empty value for `path_prompt_id` but received {path_prompt_id!r}")
        return await self._put(
            f"/configuration/prompts/prompts/{path_prompt_id}",
            body=await async_maybe_transform(
                {
                    "created_by": created_by,
                    "messages": messages,
                    "created_at": created_at,
                    "name": name,
                    "prompt_id": body_prompt_id,
                    "response_format": response_format,
                    "type": type,
                    "updated_at": updated_at,
                    "variables": variables,
                },
                prompt_update_params.PromptUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptUpdateResponse,
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
    ) -> PromptListResponse:
        """List Prompts"""
        return await self._get(
            "/configuration/prompts/prompts",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptListResponse,
        )

    async def delete(
        self,
        prompt_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not prompt_id:
            raise ValueError(f"Expected a non-empty value for `prompt_id` but received {prompt_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/configuration/prompts/prompts/{prompt_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class PromptsResourceWithRawResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create = to_raw_response_wrapper(
            prompts.create,
        )
        self.retrieve = to_raw_response_wrapper(
            prompts.retrieve,
        )
        self.update = to_raw_response_wrapper(
            prompts.update,
        )
        self.list = to_raw_response_wrapper(
            prompts.list,
        )
        self.delete = to_raw_response_wrapper(
            prompts.delete,
        )


class AsyncPromptsResourceWithRawResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create = async_to_raw_response_wrapper(
            prompts.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            prompts.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            prompts.update,
        )
        self.list = async_to_raw_response_wrapper(
            prompts.list,
        )
        self.delete = async_to_raw_response_wrapper(
            prompts.delete,
        )


class PromptsResourceWithStreamingResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create = to_streamed_response_wrapper(
            prompts.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            prompts.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            prompts.update,
        )
        self.list = to_streamed_response_wrapper(
            prompts.list,
        )
        self.delete = to_streamed_response_wrapper(
            prompts.delete,
        )


class AsyncPromptsResourceWithStreamingResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create = async_to_streamed_response_wrapper(
            prompts.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            prompts.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            prompts.update,
        )
        self.list = async_to_streamed_response_wrapper(
            prompts.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            prompts.delete,
        )
