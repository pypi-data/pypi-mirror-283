# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from tests.utils import assert_matches_type
from marly.types.integrations import (
    DestinationRegisterS3Response,
    DestinationRegisterExcelResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDestinations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_register_excel(self, client: Marly) -> None:
        destination = client.integrations.destinations.register_excel(
            data_source="string",
            output_filename="string",
        )
        assert_matches_type(DestinationRegisterExcelResponse, destination, path=["response"])

    @parametrize
    def test_raw_response_register_excel(self, client: Marly) -> None:
        response = client.integrations.destinations.with_raw_response.register_excel(
            data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = response.parse()
        assert_matches_type(DestinationRegisterExcelResponse, destination, path=["response"])

    @parametrize
    def test_streaming_response_register_excel(self, client: Marly) -> None:
        with client.integrations.destinations.with_streaming_response.register_excel(
            data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = response.parse()
            assert_matches_type(DestinationRegisterExcelResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_register_s3(self, client: Marly) -> None:
        destination = client.integrations.destinations.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )
        assert_matches_type(DestinationRegisterS3Response, destination, path=["response"])

    @parametrize
    def test_raw_response_register_s3(self, client: Marly) -> None:
        response = client.integrations.destinations.with_raw_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = response.parse()
        assert_matches_type(DestinationRegisterS3Response, destination, path=["response"])

    @parametrize
    def test_streaming_response_register_s3(self, client: Marly) -> None:
        with client.integrations.destinations.with_streaming_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = response.parse()
            assert_matches_type(DestinationRegisterS3Response, destination, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDestinations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_register_excel(self, async_client: AsyncMarly) -> None:
        destination = await async_client.integrations.destinations.register_excel(
            data_source="string",
            output_filename="string",
        )
        assert_matches_type(DestinationRegisterExcelResponse, destination, path=["response"])

    @parametrize
    async def test_raw_response_register_excel(self, async_client: AsyncMarly) -> None:
        response = await async_client.integrations.destinations.with_raw_response.register_excel(
            data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = await response.parse()
        assert_matches_type(DestinationRegisterExcelResponse, destination, path=["response"])

    @parametrize
    async def test_streaming_response_register_excel(self, async_client: AsyncMarly) -> None:
        async with async_client.integrations.destinations.with_streaming_response.register_excel(
            data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = await response.parse()
            assert_matches_type(DestinationRegisterExcelResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_register_s3(self, async_client: AsyncMarly) -> None:
        destination = await async_client.integrations.destinations.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )
        assert_matches_type(DestinationRegisterS3Response, destination, path=["response"])

    @parametrize
    async def test_raw_response_register_s3(self, async_client: AsyncMarly) -> None:
        response = await async_client.integrations.destinations.with_raw_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = await response.parse()
        assert_matches_type(DestinationRegisterS3Response, destination, path=["response"])

    @parametrize
    async def test_streaming_response_register_s3(self, async_client: AsyncMarly) -> None:
        async with async_client.integrations.destinations.with_streaming_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = await response.parse()
            assert_matches_type(DestinationRegisterS3Response, destination, path=["response"])

        assert cast(Any, response.is_closed) is True
