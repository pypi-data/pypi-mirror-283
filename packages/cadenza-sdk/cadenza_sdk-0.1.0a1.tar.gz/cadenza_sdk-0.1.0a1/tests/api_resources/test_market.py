# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import CadenzaClient, AsyncCadenzaClient
from tests.utils import assert_matches_type
from cadenza_sdk.types import MarketListInstrumentsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMarket:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list_instruments(self, client: CadenzaClient) -> None:
        market = client.market.list_instruments()
        assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

    @parametrize
    def test_method_list_instruments_with_all_params(self, client: CadenzaClient) -> None:
        market = client.market.list_instruments(
            detail=False,
            exchange_type="BINANCE",
            symbol="string",
        )
        assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

    @parametrize
    def test_raw_response_list_instruments(self, client: CadenzaClient) -> None:
        response = client.market.with_raw_response.list_instruments()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        market = response.parse()
        assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

    @parametrize
    def test_streaming_response_list_instruments(self, client: CadenzaClient) -> None:
        with client.market.with_streaming_response.list_instruments() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            market = response.parse()
            assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMarket:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list_instruments(self, async_client: AsyncCadenzaClient) -> None:
        market = await async_client.market.list_instruments()
        assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

    @parametrize
    async def test_method_list_instruments_with_all_params(self, async_client: AsyncCadenzaClient) -> None:
        market = await async_client.market.list_instruments(
            detail=False,
            exchange_type="BINANCE",
            symbol="string",
        )
        assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

    @parametrize
    async def test_raw_response_list_instruments(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.market.with_raw_response.list_instruments()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        market = await response.parse()
        assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

    @parametrize
    async def test_streaming_response_list_instruments(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.market.with_streaming_response.list_instruments() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            market = await response.parse()
            assert_matches_type(MarketListInstrumentsResponse, market, path=["response"])

        assert cast(Any, response.is_closed) is True
