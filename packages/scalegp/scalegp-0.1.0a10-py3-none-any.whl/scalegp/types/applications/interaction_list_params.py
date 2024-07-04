# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["InteractionListParams"]


class InteractionListParams(TypedDict, total=False):
    from_ts: int
    """The starting (oldest) timestamp window in seconds."""

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    search_text: str
    """Text to search for in the input/output of each interaction"""

    to_ts: int
    """The ending (most recent) timestamp in seconds."""

    variants: List[str]
    """Which variants to filter on"""
