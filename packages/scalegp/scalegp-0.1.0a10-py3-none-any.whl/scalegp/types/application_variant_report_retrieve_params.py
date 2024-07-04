# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ApplicationVariantReportRetrieveParams"]


class ApplicationVariantReportRetrieveParams(TypedDict, total=False):
    view: List[Literal["AsyncJobs"]]
