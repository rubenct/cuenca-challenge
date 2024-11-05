import time
from fastapi import APIRouter, Depends, HTTPException, status
from httpx import request
from sqlalchemy.orm import Session
from typing import List
from scr.database.connection import get_db
from scr.database.models import NQueensSolution
from scr.api.schemas import NQueensRequest, NQueensSolutionResponse, NQueensSolutionsWithCount
from scr.services.nqueens import n_queens
from scr.config.settings import settings

router = APIRouter()


@router.post(
    "/nqueens",
    response_model=NQueensSolutionsWithCount,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Solutions found or calculated successfully"},
        400: {"description": "Invalid input - n must be greater or equal than 8"},
        408: {"description": "Time has been exceeded"},
        422: {"description": "Unprocessable Entity"},
    }
)
def get_or_create_solutions(
        request: NQueensRequest,
        db: Session = Depends(get_db)
):

    if request.n < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="n must be greater or equal than 8"
        )

    # Buscar soluciones existentes en la BD
    existing_solutions = db.query(NQueensSolution).filter(
        NQueensSolution.n == request.n
    ).all()

    # Si existen soluciones, retornarlas
    if existing_solutions:
        return NQueensSolutionsWithCount(
            solutions=existing_solutions,
            comments="Data retrieved from DB",
            total_solutions=len(existing_solutions)
        )

    # Si no existen, calcular nuevas soluciones

    # Guardar soluciones en la BD
    try:
        start_time = time.time()
        db_solutions = []
        for sol in n_queens(request.n, 0, 0, 0, 0):
            if abs(time.time() - start_time) > settings.TIME_LIMIT:
                raise HTTPException(
                    status_code=status.HTTP_408_REQUEST_TIMEOUT,
                    detail=f"The {settings.TIME_LIMIT} seconds has been exceeded. 'n' must be less"
                )
            db_solutions.append(NQueensSolution(n=request.n, solution=list(sol)))

        db.add_all(db_solutions)

        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=f"Something went wrong: {str(e)}"
        )

    return NQueensSolutionsWithCount(
        comments="Data calculated successfully. POST 'n' again to show solutions",
        total_solutions=len(db_solutions)
    )
