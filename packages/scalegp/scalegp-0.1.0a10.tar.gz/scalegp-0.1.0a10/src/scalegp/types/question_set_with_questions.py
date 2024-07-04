# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from .._models import BaseModel
from .question_response import QuestionResponse

__all__ = ["QuestionSetWithQuestions"]


class QuestionSetWithQuestions(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    questions: List[QuestionResponse]
