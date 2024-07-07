# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from tests.utils import assert_matches_type
from marly._utils import parse_datetime
from marly.types.configuration import (
    NormalizationListResponse,
    NormalizationCreateResponse,
    NormalizationUpdateResponse,
    NormalizationRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNormalizations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Marly) -> None:
        normalization = client.configuration.normalizations.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )
        assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Marly) -> None:
        normalization = client.configuration.normalizations.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            description="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Marly) -> None:
        response = client.configuration.normalizations.with_raw_response.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = response.parse()
        assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Marly) -> None:
        with client.configuration.normalizations.with_streaming_response.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = response.parse()
            assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Marly) -> None:
        normalization = client.configuration.normalizations.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(NormalizationRetrieveResponse, normalization, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Marly) -> None:
        response = client.configuration.normalizations.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = response.parse()
        assert_matches_type(NormalizationRetrieveResponse, normalization, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Marly) -> None:
        with client.configuration.normalizations.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = response.parse()
            assert_matches_type(NormalizationRetrieveResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `normalization_id` but received ''"):
            client.configuration.normalizations.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Marly) -> None:
        normalization = client.configuration.normalizations.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )
        assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Marly) -> None:
        normalization = client.configuration.normalizations.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            description="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Marly) -> None:
        response = client.configuration.normalizations.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = response.parse()
        assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Marly) -> None:
        with client.configuration.normalizations.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = response.parse()
            assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `normalization_id` but received ''"):
            client.configuration.normalizations.with_raw_response.update(
                "",
                created_by="string",
                name="string",
                normalization_type="string",
                output_data_source="string",
                output_filename="string",
            )

    @parametrize
    def test_method_list(self, client: Marly) -> None:
        normalization = client.configuration.normalizations.list()
        assert_matches_type(NormalizationListResponse, normalization, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Marly) -> None:
        response = client.configuration.normalizations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = response.parse()
        assert_matches_type(NormalizationListResponse, normalization, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Marly) -> None:
        with client.configuration.normalizations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = response.parse()
            assert_matches_type(NormalizationListResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Marly) -> None:
        normalization = client.configuration.normalizations.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert normalization is None

    @parametrize
    def test_raw_response_delete(self, client: Marly) -> None:
        response = client.configuration.normalizations.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = response.parse()
        assert normalization is None

    @parametrize
    def test_streaming_response_delete(self, client: Marly) -> None:
        with client.configuration.normalizations.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = response.parse()
            assert normalization is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `normalization_id` but received ''"):
            client.configuration.normalizations.with_raw_response.delete(
                "",
            )


class TestAsyncNormalizations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMarly) -> None:
        normalization = await async_client.configuration.normalizations.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )
        assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMarly) -> None:
        normalization = await async_client.configuration.normalizations.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            description="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.normalizations.with_raw_response.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = await response.parse()
        assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.normalizations.with_streaming_response.create(
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = await response.parse()
            assert_matches_type(NormalizationCreateResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMarly) -> None:
        normalization = await async_client.configuration.normalizations.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(NormalizationRetrieveResponse, normalization, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.normalizations.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = await response.parse()
        assert_matches_type(NormalizationRetrieveResponse, normalization, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.normalizations.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = await response.parse()
            assert_matches_type(NormalizationRetrieveResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `normalization_id` but received ''"):
            await async_client.configuration.normalizations.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncMarly) -> None:
        normalization = await async_client.configuration.normalizations.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )
        assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncMarly) -> None:
        normalization = await async_client.configuration.normalizations.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            description="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.normalizations.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = await response.parse()
        assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.normalizations.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            name="string",
            normalization_type="string",
            output_data_source="string",
            output_filename="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = await response.parse()
            assert_matches_type(NormalizationUpdateResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `normalization_id` but received ''"):
            await async_client.configuration.normalizations.with_raw_response.update(
                "",
                created_by="string",
                name="string",
                normalization_type="string",
                output_data_source="string",
                output_filename="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncMarly) -> None:
        normalization = await async_client.configuration.normalizations.list()
        assert_matches_type(NormalizationListResponse, normalization, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.normalizations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = await response.parse()
        assert_matches_type(NormalizationListResponse, normalization, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.normalizations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = await response.parse()
            assert_matches_type(NormalizationListResponse, normalization, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncMarly) -> None:
        normalization = await async_client.configuration.normalizations.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert normalization is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.normalizations.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        normalization = await response.parse()
        assert normalization is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.normalizations.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            normalization = await response.parse()
            assert normalization is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `normalization_id` but received ''"):
            await async_client.configuration.normalizations.with_raw_response.delete(
                "",
            )
