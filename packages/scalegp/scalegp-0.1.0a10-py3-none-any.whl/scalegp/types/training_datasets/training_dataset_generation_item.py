# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["TrainingDatasetGenerationItem"]


class TrainingDatasetGenerationItem(BaseModel):
    input: str

    output: str

    schema_type: Optional[Literal["GENERATION"]] = None
