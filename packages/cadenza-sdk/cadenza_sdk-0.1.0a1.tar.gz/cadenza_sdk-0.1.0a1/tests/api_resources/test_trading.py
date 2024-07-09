# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import CadenzaClient, AsyncCadenzaClient
from tests.utils import assert_matches_type
from cadenza_sdk.types import (
    Order,
    QuoteExecutionReport,
    TradingListOrdersResponse,
    TradingPlaceOrderResponse,
    TradingFetchQuotesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTrading:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_cancel_order(self, client: CadenzaClient) -> None:
        trading = client.trading.cancel_order(
            order_id="string",
        )
        assert_matches_type(Order, trading, path=["response"])

    @parametrize
    def test_raw_response_cancel_order(self, client: CadenzaClient) -> None:
        response = client.trading.with_raw_response.cancel_order(
            order_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = response.parse()
        assert_matches_type(Order, trading, path=["response"])

    @parametrize
    def test_streaming_response_cancel_order(self, client: CadenzaClient) -> None:
        with client.trading.with_streaming_response.cancel_order(
            order_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = response.parse()
            assert_matches_type(Order, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_fetch_quotes_overload_1(self, client: CadenzaClient) -> None:
        trading = client.trading.fetch_quotes(
            body={},
        )
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    def test_raw_response_fetch_quotes_overload_1(self, client: CadenzaClient) -> None:
        response = client.trading.with_raw_response.fetch_quotes(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = response.parse()
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    def test_streaming_response_fetch_quotes_overload_1(self, client: CadenzaClient) -> None:
        with client.trading.with_streaming_response.fetch_quotes(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = response.parse()
            assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_fetch_quotes_overload_2(self, client: CadenzaClient) -> None:
        trading = client.trading.fetch_quotes(
            body={},
        )
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    def test_raw_response_fetch_quotes_overload_2(self, client: CadenzaClient) -> None:
        response = client.trading.with_raw_response.fetch_quotes(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = response.parse()
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    def test_streaming_response_fetch_quotes_overload_2(self, client: CadenzaClient) -> None:
        with client.trading.with_streaming_response.fetch_quotes(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = response.parse()
            assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get_quote_execution_report(self, client: CadenzaClient) -> None:
        trading = client.trading.get_quote_execution_report(
            quote_request_id="string",
        )
        assert_matches_type(QuoteExecutionReport, trading, path=["response"])

    @parametrize
    def test_raw_response_get_quote_execution_report(self, client: CadenzaClient) -> None:
        response = client.trading.with_raw_response.get_quote_execution_report(
            quote_request_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = response.parse()
        assert_matches_type(QuoteExecutionReport, trading, path=["response"])

    @parametrize
    def test_streaming_response_get_quote_execution_report(self, client: CadenzaClient) -> None:
        with client.trading.with_streaming_response.get_quote_execution_report(
            quote_request_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = response.parse()
            assert_matches_type(QuoteExecutionReport, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_orders(self, client: CadenzaClient) -> None:
        trading = client.trading.list_orders()
        assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

    @parametrize
    def test_method_list_orders_with_all_params(self, client: CadenzaClient) -> None:
        trading = client.trading.list_orders(
            end_time=1632933600000,
            exchange_account_id="string",
            limit=100,
            offset=0,
            order_id="string",
            order_status="SUBMITTED",
            start_time=1622505600000,
            symbol="string",
            tenant_id="string",
        )
        assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

    @parametrize
    def test_raw_response_list_orders(self, client: CadenzaClient) -> None:
        response = client.trading.with_raw_response.list_orders()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = response.parse()
        assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

    @parametrize
    def test_streaming_response_list_orders(self, client: CadenzaClient) -> None:
        with client.trading.with_streaming_response.list_orders() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = response.parse()
            assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_place_order_overload_1(self, client: CadenzaClient) -> None:
        trading = client.trading.place_order(
            body={},
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    def test_method_place_order_with_all_params_overload_1(self, client: CadenzaClient) -> None:
        trading = client.trading.place_order(
            body={},
            idempotency_key="my_idempotency_key",
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    def test_raw_response_place_order_overload_1(self, client: CadenzaClient) -> None:
        response = client.trading.with_raw_response.place_order(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = response.parse()
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    def test_streaming_response_place_order_overload_1(self, client: CadenzaClient) -> None:
        with client.trading.with_streaming_response.place_order(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = response.parse()
            assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_place_order_overload_2(self, client: CadenzaClient) -> None:
        trading = client.trading.place_order(
            body={},
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    def test_method_place_order_with_all_params_overload_2(self, client: CadenzaClient) -> None:
        trading = client.trading.place_order(
            body={},
            idempotency_key="my_idempotency_key",
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    def test_raw_response_place_order_overload_2(self, client: CadenzaClient) -> None:
        response = client.trading.with_raw_response.place_order(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = response.parse()
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    def test_streaming_response_place_order_overload_2(self, client: CadenzaClient) -> None:
        with client.trading.with_streaming_response.place_order(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = response.parse()
            assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTrading:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_cancel_order(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.cancel_order(
            order_id="string",
        )
        assert_matches_type(Order, trading, path=["response"])

    @parametrize
    async def test_raw_response_cancel_order(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.trading.with_raw_response.cancel_order(
            order_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = await response.parse()
        assert_matches_type(Order, trading, path=["response"])

    @parametrize
    async def test_streaming_response_cancel_order(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.trading.with_streaming_response.cancel_order(
            order_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = await response.parse()
            assert_matches_type(Order, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_fetch_quotes_overload_1(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.fetch_quotes(
            body={},
        )
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    async def test_raw_response_fetch_quotes_overload_1(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.trading.with_raw_response.fetch_quotes(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = await response.parse()
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    async def test_streaming_response_fetch_quotes_overload_1(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.trading.with_streaming_response.fetch_quotes(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = await response.parse()
            assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_fetch_quotes_overload_2(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.fetch_quotes(
            body={},
        )
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    async def test_raw_response_fetch_quotes_overload_2(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.trading.with_raw_response.fetch_quotes(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = await response.parse()
        assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

    @parametrize
    async def test_streaming_response_fetch_quotes_overload_2(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.trading.with_streaming_response.fetch_quotes(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = await response.parse()
            assert_matches_type(TradingFetchQuotesResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get_quote_execution_report(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.get_quote_execution_report(
            quote_request_id="string",
        )
        assert_matches_type(QuoteExecutionReport, trading, path=["response"])

    @parametrize
    async def test_raw_response_get_quote_execution_report(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.trading.with_raw_response.get_quote_execution_report(
            quote_request_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = await response.parse()
        assert_matches_type(QuoteExecutionReport, trading, path=["response"])

    @parametrize
    async def test_streaming_response_get_quote_execution_report(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.trading.with_streaming_response.get_quote_execution_report(
            quote_request_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = await response.parse()
            assert_matches_type(QuoteExecutionReport, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_orders(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.list_orders()
        assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

    @parametrize
    async def test_method_list_orders_with_all_params(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.list_orders(
            end_time=1632933600000,
            exchange_account_id="string",
            limit=100,
            offset=0,
            order_id="string",
            order_status="SUBMITTED",
            start_time=1622505600000,
            symbol="string",
            tenant_id="string",
        )
        assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

    @parametrize
    async def test_raw_response_list_orders(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.trading.with_raw_response.list_orders()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = await response.parse()
        assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

    @parametrize
    async def test_streaming_response_list_orders(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.trading.with_streaming_response.list_orders() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = await response.parse()
            assert_matches_type(TradingListOrdersResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_place_order_overload_1(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.place_order(
            body={},
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    async def test_method_place_order_with_all_params_overload_1(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.place_order(
            body={},
            idempotency_key="my_idempotency_key",
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    async def test_raw_response_place_order_overload_1(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.trading.with_raw_response.place_order(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = await response.parse()
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    async def test_streaming_response_place_order_overload_1(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.trading.with_streaming_response.place_order(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = await response.parse()
            assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_place_order_overload_2(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.place_order(
            body={},
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    async def test_method_place_order_with_all_params_overload_2(self, async_client: AsyncCadenzaClient) -> None:
        trading = await async_client.trading.place_order(
            body={},
            idempotency_key="my_idempotency_key",
        )
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    async def test_raw_response_place_order_overload_2(self, async_client: AsyncCadenzaClient) -> None:
        response = await async_client.trading.with_raw_response.place_order(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trading = await response.parse()
        assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

    @parametrize
    async def test_streaming_response_place_order_overload_2(self, async_client: AsyncCadenzaClient) -> None:
        async with async_client.trading.with_streaming_response.place_order(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trading = await response.parse()
            assert_matches_type(TradingPlaceOrderResponse, trading, path=["response"])

        assert cast(Any, response.is_closed) is True
