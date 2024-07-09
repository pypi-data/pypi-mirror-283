# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .order import Order
from .._models import BaseModel

__all__ = ["TradingListOrdersResponse"]


class TradingListOrdersResponse(BaseModel):
    data: Optional[List[Order]] = None

    limit: Optional[int] = None
    """Limit of the returned results"""

    offset: Optional[int] = None
    """Offset of the returned results"""

    total: Optional[int] = None
    """Total number of orders"""
