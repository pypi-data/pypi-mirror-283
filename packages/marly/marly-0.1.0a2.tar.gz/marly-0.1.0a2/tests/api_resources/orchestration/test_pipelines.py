# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPipelines:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_run_pipeline(self, client: Marly) -> None:
        pipeline = client.orchestration.pipelines.run_pipeline(
            filenames=["string", "string", "string"],
            output_mapping_ids=[
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ],
            pipeline_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, pipeline, path=["response"])

    @parametrize
    def test_raw_response_run_pipeline(self, client: Marly) -> None:
        response = client.orchestration.pipelines.with_raw_response.run_pipeline(
            filenames=["string", "string", "string"],
            output_mapping_ids=[
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ],
            pipeline_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(object, pipeline, path=["response"])

    @parametrize
    def test_streaming_response_run_pipeline(self, client: Marly) -> None:
        with client.orchestration.pipelines.with_streaming_response.run_pipeline(
            filenames=["string", "string", "string"],
            output_mapping_ids=[
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ],
            pipeline_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(object, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPipelines:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_run_pipeline(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.orchestration.pipelines.run_pipeline(
            filenames=["string", "string", "string"],
            output_mapping_ids=[
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ],
            pipeline_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, pipeline, path=["response"])

    @parametrize
    async def test_raw_response_run_pipeline(self, async_client: AsyncMarly) -> None:
        response = await async_client.orchestration.pipelines.with_raw_response.run_pipeline(
            filenames=["string", "string", "string"],
            output_mapping_ids=[
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ],
            pipeline_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(object, pipeline, path=["response"])

    @parametrize
    async def test_streaming_response_run_pipeline(self, async_client: AsyncMarly) -> None:
        async with async_client.orchestration.pipelines.with_streaming_response.run_pipeline(
            filenames=["string", "string", "string"],
            output_mapping_ids=[
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ],
            pipeline_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(object, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True
