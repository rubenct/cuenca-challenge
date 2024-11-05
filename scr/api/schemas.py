from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

#Model to request the data in the endpoint
class NQueensRequest(BaseModel):
    n: int = Field(
        ...,
        description="Number of queens to place on the board",
        le=20
    )
    show_solutions: bool = Field(
        ...,
        description="Show all solutions True:Yes"
    )

#Model base to get data
class NQueensSolutionBase(BaseModel):
    n: int
    solution: List[int]

class NQueensSolutionResponse(NQueensSolutionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

#Data format to show data
class NQueensSolutionsWithCount(BaseModel):
    solutions:  Optional[List[NQueensSolutionResponse]] = None
    total_solutions: int
    comments: str