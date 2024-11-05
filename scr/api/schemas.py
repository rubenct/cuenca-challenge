from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class NQueensRequest(BaseModel):
    n: int = Field(
        ...,
        description="Number of queens to place on the board",
        le=20,
    )

class NQueensSolutionBase(BaseModel):
    n: int
    solution: List[int]

class NQueensSolutionResponse(NQueensSolutionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class NQueensSolutionsWithCount(BaseModel):
    total_solutions: int
    comments: str
    solutions:  Optional[List[NQueensSolutionResponse]] = None

