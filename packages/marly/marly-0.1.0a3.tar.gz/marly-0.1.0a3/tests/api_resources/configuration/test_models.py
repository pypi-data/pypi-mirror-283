# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from tests.utils import assert_matches_type
from marly._utils import parse_datetime
from marly.types.configuration import (
    ModelListResponse,
    ModelCreateResponse,
    ModelUpdateResponse,
    ModelRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Marly) -> None:
        model = client.configuration.models.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )
        assert_matches_type(ModelCreateResponse, model, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Marly) -> None:
        model = client.configuration.models.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ModelCreateResponse, model, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Marly) -> None:
        response = client.configuration.models.with_raw_response.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelCreateResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Marly) -> None:
        with client.configuration.models.with_streaming_response.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelCreateResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Marly) -> None:
        model = client.configuration.models.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ModelRetrieveResponse, model, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Marly) -> None:
        response = client.configuration.models.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelRetrieveResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Marly) -> None:
        with client.configuration.models.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelRetrieveResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.configuration.models.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Marly) -> None:
        model = client.configuration.models.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )
        assert_matches_type(ModelUpdateResponse, model, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Marly) -> None:
        model = client.configuration.models.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ModelUpdateResponse, model, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Marly) -> None:
        response = client.configuration.models.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelUpdateResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Marly) -> None:
        with client.configuration.models.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelUpdateResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.configuration.models.with_raw_response.update(
                "",
                api_key="string",
                created_by="string",
                model_name="string",
                model_type="string",
            )

    @parametrize
    def test_method_list(self, client: Marly) -> None:
        model = client.configuration.models.list()
        assert_matches_type(ModelListResponse, model, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Marly) -> None:
        response = client.configuration.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelListResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Marly) -> None:
        with client.configuration.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelListResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Marly) -> None:
        model = client.configuration.models.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert model is None

    @parametrize
    def test_raw_response_delete(self, client: Marly) -> None:
        response = client.configuration.models.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert model is None

    @parametrize
    def test_streaming_response_delete(self, client: Marly) -> None:
        with client.configuration.models.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.configuration.models.with_raw_response.delete(
                "",
            )


class TestAsyncModels:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMarly) -> None:
        model = await async_client.configuration.models.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )
        assert_matches_type(ModelCreateResponse, model, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMarly) -> None:
        model = await async_client.configuration.models.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ModelCreateResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.models.with_raw_response.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelCreateResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.models.with_streaming_response.create(
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelCreateResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMarly) -> None:
        model = await async_client.configuration.models.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ModelRetrieveResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.models.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelRetrieveResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.models.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelRetrieveResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.configuration.models.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncMarly) -> None:
        model = await async_client.configuration.models.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )
        assert_matches_type(ModelUpdateResponse, model, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncMarly) -> None:
        model = await async_client.configuration.models.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
            additional_params={"foo": "string"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ModelUpdateResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.models.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelUpdateResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.models.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            api_key="string",
            created_by="string",
            model_name="string",
            model_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelUpdateResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.configuration.models.with_raw_response.update(
                "",
                api_key="string",
                created_by="string",
                model_name="string",
                model_type="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncMarly) -> None:
        model = await async_client.configuration.models.list()
        assert_matches_type(ModelListResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelListResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelListResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncMarly) -> None:
        model = await async_client.configuration.models.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert model is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.models.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert model is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.models.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.configuration.models.with_raw_response.delete(
                "",
            )
