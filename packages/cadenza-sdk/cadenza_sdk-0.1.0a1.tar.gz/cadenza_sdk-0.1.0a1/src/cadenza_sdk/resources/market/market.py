# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .kline import (
    KlineResource,
    AsyncKlineResource,
    KlineResourceWithRawResponse,
    AsyncKlineResourceWithRawResponse,
    KlineResourceWithStreamingResponse,
    AsyncKlineResourceWithStreamingResponse,
)
from .ticker import (
    TickerResource,
    AsyncTickerResource,
    TickerResourceWithRawResponse,
    AsyncTickerResourceWithRawResponse,
    TickerResourceWithStreamingResponse,
    AsyncTickerResourceWithStreamingResponse,
)
from ...types import market_list_instruments_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .orderbook import (
    OrderbookResource,
    AsyncOrderbookResource,
    OrderbookResourceWithRawResponse,
    AsyncOrderbookResourceWithRawResponse,
    OrderbookResourceWithStreamingResponse,
    AsyncOrderbookResourceWithStreamingResponse,
)
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
from ...types.market_list_instruments_response import MarketListInstrumentsResponse

__all__ = ["MarketResource", "AsyncMarketResource"]


class MarketResource(SyncAPIResource):
    @cached_property
    def ticker(self) -> TickerResource:
        return TickerResource(self._client)

    @cached_property
    def orderbook(self) -> OrderbookResource:
        return OrderbookResource(self._client)

    @cached_property
    def kline(self) -> KlineResource:
        return KlineResource(self._client)

    @cached_property
    def with_raw_response(self) -> MarketResourceWithRawResponse:
        return MarketResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MarketResourceWithStreamingResponse:
        return MarketResourceWithStreamingResponse(self)

    def list_instruments(
        self,
        *,
        detail: bool | NotGiven = NOT_GIVEN,
        exchange_type: Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"]
        | NotGiven = NOT_GIVEN,
        symbol: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MarketListInstrumentsResponse:
        """
        List available exchange symbols

        Args:
          detail: Whether to return detailed information

          exchange_type: Exchange type

          symbol: Symbol

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v2/market/listSymbolInfo",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "detail": detail,
                        "exchange_type": exchange_type,
                        "symbol": symbol,
                    },
                    market_list_instruments_params.MarketListInstrumentsParams,
                ),
            ),
            cast_to=MarketListInstrumentsResponse,
        )


class AsyncMarketResource(AsyncAPIResource):
    @cached_property
    def ticker(self) -> AsyncTickerResource:
        return AsyncTickerResource(self._client)

    @cached_property
    def orderbook(self) -> AsyncOrderbookResource:
        return AsyncOrderbookResource(self._client)

    @cached_property
    def kline(self) -> AsyncKlineResource:
        return AsyncKlineResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMarketResourceWithRawResponse:
        return AsyncMarketResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMarketResourceWithStreamingResponse:
        return AsyncMarketResourceWithStreamingResponse(self)

    async def list_instruments(
        self,
        *,
        detail: bool | NotGiven = NOT_GIVEN,
        exchange_type: Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"]
        | NotGiven = NOT_GIVEN,
        symbol: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MarketListInstrumentsResponse:
        """
        List available exchange symbols

        Args:
          detail: Whether to return detailed information

          exchange_type: Exchange type

          symbol: Symbol

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v2/market/listSymbolInfo",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "detail": detail,
                        "exchange_type": exchange_type,
                        "symbol": symbol,
                    },
                    market_list_instruments_params.MarketListInstrumentsParams,
                ),
            ),
            cast_to=MarketListInstrumentsResponse,
        )


class MarketResourceWithRawResponse:
    def __init__(self, market: MarketResource) -> None:
        self._market = market

        self.list_instruments = to_raw_response_wrapper(
            market.list_instruments,
        )

    @cached_property
    def ticker(self) -> TickerResourceWithRawResponse:
        return TickerResourceWithRawResponse(self._market.ticker)

    @cached_property
    def orderbook(self) -> OrderbookResourceWithRawResponse:
        return OrderbookResourceWithRawResponse(self._market.orderbook)

    @cached_property
    def kline(self) -> KlineResourceWithRawResponse:
        return KlineResourceWithRawResponse(self._market.kline)


class AsyncMarketResourceWithRawResponse:
    def __init__(self, market: AsyncMarketResource) -> None:
        self._market = market

        self.list_instruments = async_to_raw_response_wrapper(
            market.list_instruments,
        )

    @cached_property
    def ticker(self) -> AsyncTickerResourceWithRawResponse:
        return AsyncTickerResourceWithRawResponse(self._market.ticker)

    @cached_property
    def orderbook(self) -> AsyncOrderbookResourceWithRawResponse:
        return AsyncOrderbookResourceWithRawResponse(self._market.orderbook)

    @cached_property
    def kline(self) -> AsyncKlineResourceWithRawResponse:
        return AsyncKlineResourceWithRawResponse(self._market.kline)


class MarketResourceWithStreamingResponse:
    def __init__(self, market: MarketResource) -> None:
        self._market = market

        self.list_instruments = to_streamed_response_wrapper(
            market.list_instruments,
        )

    @cached_property
    def ticker(self) -> TickerResourceWithStreamingResponse:
        return TickerResourceWithStreamingResponse(self._market.ticker)

    @cached_property
    def orderbook(self) -> OrderbookResourceWithStreamingResponse:
        return OrderbookResourceWithStreamingResponse(self._market.orderbook)

    @cached_property
    def kline(self) -> KlineResourceWithStreamingResponse:
        return KlineResourceWithStreamingResponse(self._market.kline)


class AsyncMarketResourceWithStreamingResponse:
    def __init__(self, market: AsyncMarketResource) -> None:
        self._market = market

        self.list_instruments = async_to_streamed_response_wrapper(
            market.list_instruments,
        )

    @cached_property
    def ticker(self) -> AsyncTickerResourceWithStreamingResponse:
        return AsyncTickerResourceWithStreamingResponse(self._market.ticker)

    @cached_property
    def orderbook(self) -> AsyncOrderbookResourceWithStreamingResponse:
        return AsyncOrderbookResourceWithStreamingResponse(self._market.orderbook)

    @cached_property
    def kline(self) -> AsyncKlineResourceWithStreamingResponse:
        return AsyncKlineResourceWithStreamingResponse(self._market.kline)
