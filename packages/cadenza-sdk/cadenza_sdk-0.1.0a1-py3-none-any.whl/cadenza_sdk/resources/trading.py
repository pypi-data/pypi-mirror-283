# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast, overload
from typing_extensions import Literal

import httpx

from ..types import (
    trading_list_orders_params,
    trading_place_order_params,
    trading_cancel_order_params,
    trading_fetch_quotes_params,
    trading_get_quote_execution_report_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    required_args,
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..types.order import Order
from .._base_client import (
    make_request_options,
)
from ..types.quote_execution_report import QuoteExecutionReport
from ..types.trading_list_orders_response import TradingListOrdersResponse
from ..types.trading_place_order_response import TradingPlaceOrderResponse
from ..types.trading_fetch_quotes_response import TradingFetchQuotesResponse

__all__ = ["TradingResource", "AsyncTradingResource"]


class TradingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TradingResourceWithRawResponse:
        return TradingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TradingResourceWithStreamingResponse:
        return TradingResourceWithStreamingResponse(self)

    def cancel_order(
        self,
        *,
        order_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Order:
        """Cancel order.

        If the order is already filled, it will return an error.

        Args:
          order_id: Order ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/trading/cancelOrder",
            body=maybe_transform({"order_id": order_id}, trading_cancel_order_params.TradingCancelOrderParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Order,
        )

    @overload
    def fetch_quotes(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingFetchQuotesResponse:
        """
        Quote will give the best quote from all available exchange accounts

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def fetch_quotes(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingFetchQuotesResponse:
        """
        Quote will give the best quote from all available exchange accounts

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["body"])
    def fetch_quotes(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingFetchQuotesResponse:
        return self._post(
            "/api/v2/trading/fetchQuotes",
            body=maybe_transform(body, trading_fetch_quotes_params.TradingFetchQuotesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TradingFetchQuotesResponse,
        )

    def get_quote_execution_report(
        self,
        *,
        quote_request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuoteExecutionReport:
        """
        Quote will give the best quote from all available exchange accounts

        Args:
          quote_request_id: Quote request ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            QuoteExecutionReport,
            self._post(
                "/api/v2/trading/getQuoteExecutionReport",
                body=maybe_transform(
                    {"quote_request_id": quote_request_id},
                    trading_get_quote_execution_report_params.TradingGetQuoteExecutionReportParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, QuoteExecutionReport
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list_orders(
        self,
        *,
        end_time: int | NotGiven = NOT_GIVEN,
        exchange_account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order_id: str | NotGiven = NOT_GIVEN,
        order_status: Literal[
            "SUBMITTED",
            "ACCEPTED",
            "OPEN",
            "PARTIALLY_FILLED",
            "FILLED",
            "CANCELED",
            "PENDING_CANCEL",
            "REJECTED",
            "EXPIRED",
            "REVOKED",
        ]
        | NotGiven = NOT_GIVEN,
        start_time: int | NotGiven = NOT_GIVEN,
        symbol: str | NotGiven = NOT_GIVEN,
        tenant_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingListOrdersResponse:
        """
        List orders

        Args:
          end_time: End time (in unix milliseconds)

          exchange_account_id: Exchange account ID

          limit: Limit the number of returned results.

          offset: Offset of the returned results. Default: 0

          order_id: Order ID

          order_status: Order status

          start_time: Start time (in unix milliseconds)

          symbol: Symbol

          tenant_id: Tenant ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v2/trading/listOrders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_time": end_time,
                        "exchange_account_id": exchange_account_id,
                        "limit": limit,
                        "offset": offset,
                        "order_id": order_id,
                        "order_status": order_status,
                        "start_time": start_time,
                        "symbol": symbol,
                        "tenant_id": tenant_id,
                    },
                    trading_list_orders_params.TradingListOrdersParams,
                ),
            ),
            cast_to=TradingListOrdersResponse,
        )

    @overload
    def place_order(
        self,
        *,
        body: object,
        idempotency_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingPlaceOrderResponse:
        """
        Place order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def place_order(
        self,
        *,
        body: object,
        idempotency_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingPlaceOrderResponse:
        """
        Place order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["body"])
    def place_order(
        self,
        *,
        body: object,
        idempotency_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingPlaceOrderResponse:
        extra_headers = {**strip_not_given({"Idempotency-Key": idempotency_key}), **(extra_headers or {})}
        return self._post(
            "/api/v2/trading/placeOrder",
            body=maybe_transform(body, trading_place_order_params.TradingPlaceOrderParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TradingPlaceOrderResponse,
        )


class AsyncTradingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTradingResourceWithRawResponse:
        return AsyncTradingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTradingResourceWithStreamingResponse:
        return AsyncTradingResourceWithStreamingResponse(self)

    async def cancel_order(
        self,
        *,
        order_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Order:
        """Cancel order.

        If the order is already filled, it will return an error.

        Args:
          order_id: Order ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/trading/cancelOrder",
            body=await async_maybe_transform(
                {"order_id": order_id}, trading_cancel_order_params.TradingCancelOrderParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Order,
        )

    @overload
    async def fetch_quotes(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingFetchQuotesResponse:
        """
        Quote will give the best quote from all available exchange accounts

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def fetch_quotes(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingFetchQuotesResponse:
        """
        Quote will give the best quote from all available exchange accounts

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["body"])
    async def fetch_quotes(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingFetchQuotesResponse:
        return await self._post(
            "/api/v2/trading/fetchQuotes",
            body=await async_maybe_transform(body, trading_fetch_quotes_params.TradingFetchQuotesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TradingFetchQuotesResponse,
        )

    async def get_quote_execution_report(
        self,
        *,
        quote_request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuoteExecutionReport:
        """
        Quote will give the best quote from all available exchange accounts

        Args:
          quote_request_id: Quote request ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            QuoteExecutionReport,
            await self._post(
                "/api/v2/trading/getQuoteExecutionReport",
                body=await async_maybe_transform(
                    {"quote_request_id": quote_request_id},
                    trading_get_quote_execution_report_params.TradingGetQuoteExecutionReportParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, QuoteExecutionReport
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list_orders(
        self,
        *,
        end_time: int | NotGiven = NOT_GIVEN,
        exchange_account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order_id: str | NotGiven = NOT_GIVEN,
        order_status: Literal[
            "SUBMITTED",
            "ACCEPTED",
            "OPEN",
            "PARTIALLY_FILLED",
            "FILLED",
            "CANCELED",
            "PENDING_CANCEL",
            "REJECTED",
            "EXPIRED",
            "REVOKED",
        ]
        | NotGiven = NOT_GIVEN,
        start_time: int | NotGiven = NOT_GIVEN,
        symbol: str | NotGiven = NOT_GIVEN,
        tenant_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingListOrdersResponse:
        """
        List orders

        Args:
          end_time: End time (in unix milliseconds)

          exchange_account_id: Exchange account ID

          limit: Limit the number of returned results.

          offset: Offset of the returned results. Default: 0

          order_id: Order ID

          order_status: Order status

          start_time: Start time (in unix milliseconds)

          symbol: Symbol

          tenant_id: Tenant ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v2/trading/listOrders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_time": end_time,
                        "exchange_account_id": exchange_account_id,
                        "limit": limit,
                        "offset": offset,
                        "order_id": order_id,
                        "order_status": order_status,
                        "start_time": start_time,
                        "symbol": symbol,
                        "tenant_id": tenant_id,
                    },
                    trading_list_orders_params.TradingListOrdersParams,
                ),
            ),
            cast_to=TradingListOrdersResponse,
        )

    @overload
    async def place_order(
        self,
        *,
        body: object,
        idempotency_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingPlaceOrderResponse:
        """
        Place order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def place_order(
        self,
        *,
        body: object,
        idempotency_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingPlaceOrderResponse:
        """
        Place order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["body"])
    async def place_order(
        self,
        *,
        body: object,
        idempotency_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TradingPlaceOrderResponse:
        extra_headers = {**strip_not_given({"Idempotency-Key": idempotency_key}), **(extra_headers or {})}
        return await self._post(
            "/api/v2/trading/placeOrder",
            body=await async_maybe_transform(body, trading_place_order_params.TradingPlaceOrderParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TradingPlaceOrderResponse,
        )


class TradingResourceWithRawResponse:
    def __init__(self, trading: TradingResource) -> None:
        self._trading = trading

        self.cancel_order = to_raw_response_wrapper(
            trading.cancel_order,
        )
        self.fetch_quotes = to_raw_response_wrapper(
            trading.fetch_quotes,
        )
        self.get_quote_execution_report = to_raw_response_wrapper(
            trading.get_quote_execution_report,
        )
        self.list_orders = to_raw_response_wrapper(
            trading.list_orders,
        )
        self.place_order = to_raw_response_wrapper(
            trading.place_order,
        )


class AsyncTradingResourceWithRawResponse:
    def __init__(self, trading: AsyncTradingResource) -> None:
        self._trading = trading

        self.cancel_order = async_to_raw_response_wrapper(
            trading.cancel_order,
        )
        self.fetch_quotes = async_to_raw_response_wrapper(
            trading.fetch_quotes,
        )
        self.get_quote_execution_report = async_to_raw_response_wrapper(
            trading.get_quote_execution_report,
        )
        self.list_orders = async_to_raw_response_wrapper(
            trading.list_orders,
        )
        self.place_order = async_to_raw_response_wrapper(
            trading.place_order,
        )


class TradingResourceWithStreamingResponse:
    def __init__(self, trading: TradingResource) -> None:
        self._trading = trading

        self.cancel_order = to_streamed_response_wrapper(
            trading.cancel_order,
        )
        self.fetch_quotes = to_streamed_response_wrapper(
            trading.fetch_quotes,
        )
        self.get_quote_execution_report = to_streamed_response_wrapper(
            trading.get_quote_execution_report,
        )
        self.list_orders = to_streamed_response_wrapper(
            trading.list_orders,
        )
        self.place_order = to_streamed_response_wrapper(
            trading.place_order,
        )


class AsyncTradingResourceWithStreamingResponse:
    def __init__(self, trading: AsyncTradingResource) -> None:
        self._trading = trading

        self.cancel_order = async_to_streamed_response_wrapper(
            trading.cancel_order,
        )
        self.fetch_quotes = async_to_streamed_response_wrapper(
            trading.fetch_quotes,
        )
        self.get_quote_execution_report = async_to_streamed_response_wrapper(
            trading.get_quote_execution_report,
        )
        self.list_orders = async_to_streamed_response_wrapper(
            trading.list_orders,
        )
        self.place_order = async_to_streamed_response_wrapper(
            trading.place_order,
        )
