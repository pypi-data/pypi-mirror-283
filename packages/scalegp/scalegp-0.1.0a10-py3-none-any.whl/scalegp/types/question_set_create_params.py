# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["QuestionSetCreateParams"]


class QuestionSetCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    name: Required[str]

    question_ids: Required[List[str]]
    """IDs of questions in the question set"""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
