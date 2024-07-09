# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .order import Order
from .._models import BaseModel

__all__ = ["QuoteExecutionReport", "UnionMember0", "UnionMember0Fee", "UnionMember1", "UnionMember1Fee", "UnionMember2"]


class UnionMember0Fee(BaseModel):
    asset: Optional[str] = None
    """Asset"""

    quantity: Optional[float] = None
    """Quantity"""


class UnionMember0(BaseModel):
    base_currency: Optional[str] = FieldInfo(alias="baseCurrency", default=None)
    """Base currency"""

    cl_ord_id: Optional[str] = FieldInfo(alias="clOrdId", default=None)
    """Order request ID, Client Order ID"""

    cost: Optional[float] = None
    """Cost, the total cost of the quote"""

    created_at: Optional[int] = FieldInfo(alias="createdAt", default=None)
    """Create time of the quote"""

    executions: Optional[List[Order]] = None
    """
    List of executions to fulfill the order, the order status should only have
    FILLED, REJECTED, or EXPIRED
    """

    fees: Optional[List[UnionMember0Fee]] = None
    """Fees"""

    filled: Optional[float] = None
    """Filled quantity, the quantity of the base currency executed"""

    order: Optional[Order] = None

    quote_currency: Optional[str] = FieldInfo(alias="quoteCurrency", default=None)
    """Quote currency"""

    route_policy: Optional[Literal["PRIORITY", "QUOTE"]] = FieldInfo(alias="routePolicy", default=None)
    """Route policy.

    For PRIORITY, the order request will be routed to the exchange account with the
    highest priority. For QUOTE, the system will execute the execution plan based on
    the quote. Order request with route policy QUOTE will only accept two
    parameters, quoteRequestId and priceSlippageTolerance
    """

    status: Optional[
        Literal[
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
    ] = None
    """
    Status of the quote execution, should only have SUBMITTED, ACCEPTED,
    PARTIALLY_FILLED, FILLED, EXPIRED. the final status of the quote execution
    should be either FILLED or EXPIRED
    """

    updated_at: Optional[int] = FieldInfo(alias="updatedAt", default=None)
    """Last updated time of the quote execution"""


class UnionMember1Fee(BaseModel):
    asset: Optional[str] = None
    """Asset"""

    quantity: Optional[float] = None
    """Quantity"""


class UnionMember1(BaseModel):
    base_currency: Optional[str] = FieldInfo(alias="baseCurrency", default=None)
    """Base currency"""

    cl_ord_id: Optional[str] = FieldInfo(alias="clOrdId", default=None)
    """Order request ID, Client Order ID"""

    cost: Optional[float] = None
    """Cost, the total cost of the quote"""

    created_at: Optional[int] = FieldInfo(alias="createdAt", default=None)
    """Create time of the quote"""

    executions: Optional[List[Order]] = None
    """
    List of executions to fulfill the order, the order status should only have
    FILLED, REJECTED, or EXPIRED
    """

    fees: Optional[List[UnionMember1Fee]] = None
    """Fees"""

    filled: Optional[float] = None
    """Filled quantity, the quantity of the base currency executed"""

    order: Optional[Order] = None

    quote_currency: Optional[str] = FieldInfo(alias="quoteCurrency", default=None)
    """Quote currency"""

    route_policy: Optional[Literal["PRIORITY", "QUOTE"]] = FieldInfo(alias="routePolicy", default=None)
    """Route policy.

    For PRIORITY, the order request will be routed to the exchange account with the
    highest priority. For QUOTE, the system will execute the execution plan based on
    the quote. Order request with route policy QUOTE will only accept two
    parameters, quoteRequestId and priceSlippageTolerance
    """

    status: Optional[
        Literal[
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
    ] = None
    """
    Status of the quote execution, should only have SUBMITTED, ACCEPTED,
    PARTIALLY_FILLED, FILLED, EXPIRED. the final status of the quote execution
    should be either FILLED or EXPIRED
    """

    updated_at: Optional[int] = FieldInfo(alias="updatedAt", default=None)
    """Last updated time of the quote execution"""


class UnionMember2(BaseModel):
    quote_request_id: str = FieldInfo(alias="quoteRequestId")
    """Quote request ID"""

    valid_until: int = FieldInfo(alias="validUntil")
    """Expiration time of the quote"""


QuoteExecutionReport = Union[UnionMember0, UnionMember1, UnionMember2]
