# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from marly.types import RegisterIntegrationResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestIntegrations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_register_excel(self, client: Marly) -> None:
        integration = client.integrations.register_excel(
            data_source="string",
            output_filename="string",
        )
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    def test_raw_response_register_excel(self, client: Marly) -> None:
        response = client.integrations.with_raw_response.register_excel(
            data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        integration = response.parse()
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    def test_streaming_response_register_excel(self, client: Marly) -> None:
        with client.integrations.with_streaming_response.register_excel(
            data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            integration = response.parse()
            assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_register_s3(self, client: Marly) -> None:
        integration = client.integrations.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    def test_raw_response_register_s3(self, client: Marly) -> None:
        response = client.integrations.with_raw_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        integration = response.parse()
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    def test_streaming_response_register_s3(self, client: Marly) -> None:
        with client.integrations.with_streaming_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            integration = response.parse()
            assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncIntegrations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_register_excel(self, async_client: AsyncMarly) -> None:
        integration = await async_client.integrations.register_excel(
            data_source="string",
            output_filename="string",
        )
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    async def test_raw_response_register_excel(self, async_client: AsyncMarly) -> None:
        response = await async_client.integrations.with_raw_response.register_excel(
            data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        integration = await response.parse()
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    async def test_streaming_response_register_excel(self, async_client: AsyncMarly) -> None:
        async with async_client.integrations.with_streaming_response.register_excel(
            data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            integration = await response.parse()
            assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_register_s3(self, async_client: AsyncMarly) -> None:
        integration = await async_client.integrations.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    async def test_raw_response_register_s3(self, async_client: AsyncMarly) -> None:
        response = await async_client.integrations.with_raw_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        integration = await response.parse()
        assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

    @parametrize
    async def test_streaming_response_register_s3(self, async_client: AsyncMarly) -> None:
        async with async_client.integrations.with_streaming_response.register_s3(
            aws_access_key="string",
            aws_secret_key="string",
            bucket_name="string",
            region_name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            integration = await response.parse()
            assert_matches_type(RegisterIntegrationResponse, integration, path=["response"])

        assert cast(Any, response.is_closed) is True
