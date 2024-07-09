# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TradingPlaceOrderParams", "Variant0", "Variant1"]


class Variant0(TypedDict, total=False):
    body: Required[object]

    idempotency_key: Annotated[str, PropertyInfo(alias="Idempotency-Key")]


class Variant1(TypedDict, total=False):
    body: Required[object]

    idempotency_key: Annotated[str, PropertyInfo(alias="Idempotency-Key")]


TradingPlaceOrderParams = Union[Variant0, Variant1]
