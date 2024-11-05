from sqlalchemy import Column, Integer, ARRAY, DateTime
from sqlalchemy.sql import func
from scr.database.connection import Base

class NQueensSolution(Base):
    __tablename__ = "nqueens_solutions"

    id = Column(Integer, primary_key=True, index=True)
    n = Column(Integer)
    solution = Column(ARRAY(Integer))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

#