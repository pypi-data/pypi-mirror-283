# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from tests.utils import assert_matches_type
from marly._utils import parse_datetime
from marly.types.configuration import (
    OutputMappingListResponse,
    OutputMappingCreateResponse,
    OutputMappingUpdateResponse,
    OutputMappingRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOutputMappings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Marly) -> None:
        output_mapping = client.configuration.output_mappings.create(
            created_by="string",
        )
        assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Marly) -> None:
        output_mapping = client.configuration.output_mappings.create(
            created_by="string",
            column_locations={"foo": {"foo": "string"}},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            data_locations=["string", "string", "string"],
            output_data_type="string",
            output_filename="string",
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Marly) -> None:
        response = client.configuration.output_mappings.with_raw_response.create(
            created_by="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = response.parse()
        assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Marly) -> None:
        with client.configuration.output_mappings.with_streaming_response.create(
            created_by="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = response.parse()
            assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Marly) -> None:
        output_mapping = client.configuration.output_mappings.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OutputMappingRetrieveResponse, output_mapping, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Marly) -> None:
        response = client.configuration.output_mappings.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = response.parse()
        assert_matches_type(OutputMappingRetrieveResponse, output_mapping, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Marly) -> None:
        with client.configuration.output_mappings.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = response.parse()
            assert_matches_type(OutputMappingRetrieveResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `output_mapping_id` but received ''"):
            client.configuration.output_mappings.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Marly) -> None:
        output_mapping = client.configuration.output_mappings.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
        )
        assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Marly) -> None:
        output_mapping = client.configuration.output_mappings.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            column_locations={"foo": {"foo": "string"}},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            data_locations=["string", "string", "string"],
            output_data_type="string",
            output_filename="string",
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Marly) -> None:
        response = client.configuration.output_mappings.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = response.parse()
        assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Marly) -> None:
        with client.configuration.output_mappings.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = response.parse()
            assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `output_mapping_id` but received ''"):
            client.configuration.output_mappings.with_raw_response.update(
                "",
                created_by="string",
            )

    @parametrize
    def test_method_list(self, client: Marly) -> None:
        output_mapping = client.configuration.output_mappings.list()
        assert_matches_type(OutputMappingListResponse, output_mapping, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Marly) -> None:
        response = client.configuration.output_mappings.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = response.parse()
        assert_matches_type(OutputMappingListResponse, output_mapping, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Marly) -> None:
        with client.configuration.output_mappings.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = response.parse()
            assert_matches_type(OutputMappingListResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Marly) -> None:
        output_mapping = client.configuration.output_mappings.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert output_mapping is None

    @parametrize
    def test_raw_response_delete(self, client: Marly) -> None:
        response = client.configuration.output_mappings.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = response.parse()
        assert output_mapping is None

    @parametrize
    def test_streaming_response_delete(self, client: Marly) -> None:
        with client.configuration.output_mappings.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = response.parse()
            assert output_mapping is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `output_mapping_id` but received ''"):
            client.configuration.output_mappings.with_raw_response.delete(
                "",
            )


class TestAsyncOutputMappings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMarly) -> None:
        output_mapping = await async_client.configuration.output_mappings.create(
            created_by="string",
        )
        assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMarly) -> None:
        output_mapping = await async_client.configuration.output_mappings.create(
            created_by="string",
            column_locations={"foo": {"foo": "string"}},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            data_locations=["string", "string", "string"],
            output_data_type="string",
            output_filename="string",
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.output_mappings.with_raw_response.create(
            created_by="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = await response.parse()
        assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.output_mappings.with_streaming_response.create(
            created_by="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = await response.parse()
            assert_matches_type(OutputMappingCreateResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMarly) -> None:
        output_mapping = await async_client.configuration.output_mappings.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OutputMappingRetrieveResponse, output_mapping, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.output_mappings.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = await response.parse()
        assert_matches_type(OutputMappingRetrieveResponse, output_mapping, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.output_mappings.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = await response.parse()
            assert_matches_type(OutputMappingRetrieveResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `output_mapping_id` but received ''"):
            await async_client.configuration.output_mappings.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncMarly) -> None:
        output_mapping = await async_client.configuration.output_mappings.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
        )
        assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncMarly) -> None:
        output_mapping = await async_client.configuration.output_mappings.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            column_locations={"foo": {"foo": "string"}},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            data_locations=["string", "string", "string"],
            output_data_type="string",
            output_filename="string",
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.output_mappings.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = await response.parse()
        assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.output_mappings.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = await response.parse()
            assert_matches_type(OutputMappingUpdateResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `output_mapping_id` but received ''"):
            await async_client.configuration.output_mappings.with_raw_response.update(
                "",
                created_by="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncMarly) -> None:
        output_mapping = await async_client.configuration.output_mappings.list()
        assert_matches_type(OutputMappingListResponse, output_mapping, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.output_mappings.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = await response.parse()
        assert_matches_type(OutputMappingListResponse, output_mapping, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.output_mappings.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = await response.parse()
            assert_matches_type(OutputMappingListResponse, output_mapping, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncMarly) -> None:
        output_mapping = await async_client.configuration.output_mappings.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert output_mapping is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.output_mappings.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        output_mapping = await response.parse()
        assert output_mapping is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.output_mappings.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            output_mapping = await response.parse()
            assert output_mapping is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `output_mapping_id` but received ''"):
            await async_client.configuration.output_mappings.with_raw_response.delete(
                "",
            )
