# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ExecutionReportGetQuoteExecutionReportParams"]


class ExecutionReportGetQuoteExecutionReportParams(TypedDict, total=False):
    quote_request_id: Required[Annotated[str, PropertyInfo(alias="quoteRequestId")]]
    """Quote request ID"""
