# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from tests.utils import assert_matches_type
from marly._utils import parse_datetime
from marly.types.configuration import (
    PipelineListResponse,
    PipelineCreateResponse,
    PipelineUpdateResponse,
    PipelineRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPipelines:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Marly) -> None:
        pipeline = client.configuration.pipelines.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )
        assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Marly) -> None:
        pipeline = client.configuration.pipelines.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            integrations={"foo": "string"},
            normalization_id="string",
            prompt_ids={"foo": "string"},
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Marly) -> None:
        response = client.configuration.pipelines.with_raw_response.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Marly) -> None:
        with client.configuration.pipelines.with_streaming_response.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Marly) -> None:
        pipeline = client.configuration.pipelines.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PipelineRetrieveResponse, pipeline, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Marly) -> None:
        response = client.configuration.pipelines.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(PipelineRetrieveResponse, pipeline, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Marly) -> None:
        with client.configuration.pipelines.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(PipelineRetrieveResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            client.configuration.pipelines.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Marly) -> None:
        pipeline = client.configuration.pipelines.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )
        assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Marly) -> None:
        pipeline = client.configuration.pipelines.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            integrations={"foo": "string"},
            normalization_id="string",
            prompt_ids={"foo": "string"},
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Marly) -> None:
        response = client.configuration.pipelines.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Marly) -> None:
        with client.configuration.pipelines.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            client.configuration.pipelines.with_raw_response.update(
                "",
                created_by="string",
                model_id="string",
                name="string",
                pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                run_type="string",
            )

    @parametrize
    def test_method_list(self, client: Marly) -> None:
        pipeline = client.configuration.pipelines.list()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Marly) -> None:
        response = client.configuration.pipelines.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Marly) -> None:
        with client.configuration.pipelines.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(PipelineListResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Marly) -> None:
        pipeline = client.configuration.pipelines.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert pipeline is None

    @parametrize
    def test_raw_response_delete(self, client: Marly) -> None:
        response = client.configuration.pipelines.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert pipeline is None

    @parametrize
    def test_streaming_response_delete(self, client: Marly) -> None:
        with client.configuration.pipelines.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert pipeline is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            client.configuration.pipelines.with_raw_response.delete(
                "",
            )


class TestAsyncPipelines:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.configuration.pipelines.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )
        assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.configuration.pipelines.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            integrations={"foo": "string"},
            normalization_id="string",
            prompt_ids={"foo": "string"},
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.pipelines.with_raw_response.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.pipelines.with_streaming_response.create(
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(PipelineCreateResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.configuration.pipelines.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PipelineRetrieveResponse, pipeline, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.pipelines.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(PipelineRetrieveResponse, pipeline, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.pipelines.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(PipelineRetrieveResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            await async_client.configuration.pipelines.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.configuration.pipelines.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )
        assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.configuration.pipelines.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            integrations={"foo": "string"},
            normalization_id="string",
            prompt_ids={"foo": "string"},
            status="string",
            updated_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.pipelines.with_raw_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.pipelines.with_streaming_response.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_by="string",
            model_id="string",
            name="string",
            pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            run_type="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(PipelineUpdateResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            await async_client.configuration.pipelines.with_raw_response.update(
                "",
                created_by="string",
                model_id="string",
                name="string",
                pipeline_schema_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                run_type="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.configuration.pipelines.list()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.pipelines.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.pipelines.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(PipelineListResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.configuration.pipelines.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert pipeline is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncMarly) -> None:
        response = await async_client.configuration.pipelines.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert pipeline is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncMarly) -> None:
        async with async_client.configuration.pipelines.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert pipeline is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            await async_client.configuration.pipelines.with_raw_response.delete(
                "",
            )
