# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EvaluationConfigCreateParams"]


class EvaluationConfigCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    evaluation_type: Required[Literal["studio", "llm_auto", "human", "llm_benchmark"]]
    """An enumeration."""

    question_set_id: Required[str]

    studio_project_id: str

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
