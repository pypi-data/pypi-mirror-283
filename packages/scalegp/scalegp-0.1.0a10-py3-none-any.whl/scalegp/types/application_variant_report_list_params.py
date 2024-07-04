# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ApplicationVariantReportListParams"]


class ApplicationVariantReportListParams(TypedDict, total=False):
    account_id: str

    application_spec_id: str

    application_variant_id: str

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    view: List[Literal["AsyncJobs"]]

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
