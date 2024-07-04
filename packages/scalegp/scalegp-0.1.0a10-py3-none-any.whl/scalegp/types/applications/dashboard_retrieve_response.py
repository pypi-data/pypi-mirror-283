# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["DashboardRetrieveResponse", "Visualization"]


class Visualization(BaseModel):
    id: str

    metric_id: Literal[
        "total_requests",
        "total_errors",
        "total_tokens",
        "average_latency",
        "p95_latency",
        "error_rate",
        "inference_calls",
        "average_users",
        "aggregated_tokens",
        "feedback",
    ]
    """An enumeration."""

    title: str

    type: Literal["scalar", "bar", "stacked_bar", "line"]
    """An enumeration."""


class DashboardRetrieveResponse(BaseModel):
    id: str

    title: str

    visualizations: List[Visualization]
