# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["UploadScheduleRetrieveParams"]


class UploadScheduleRetrieveParams(TypedDict, total=False):
    knowledge_base_id: Required[str]

    view: List[Literal["DataSource"]]
