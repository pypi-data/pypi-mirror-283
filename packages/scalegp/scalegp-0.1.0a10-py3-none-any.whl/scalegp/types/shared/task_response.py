# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .test_case_result_response import TestCaseResultResponse

__all__ = ["TaskResponse"]


class TaskResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    priority: int

    status: Literal["PENDING", "COMPLETED"]
    """An enumeration."""

    task_entity_id: str

    task_entity_parent_id: str

    task_type: Literal["EVALUATION_ANNOTATION"]
    """An enumeration."""

    assigned_to: Optional[str] = None
    """The ID of the user that the task is assigned to."""

    assignment_expires_at: Optional[datetime] = None
    """The date and time when the task assignment expires in ISO format."""

    task_entity: Optional[TestCaseResultResponse] = None
    """The entity that the task is associated with."""
