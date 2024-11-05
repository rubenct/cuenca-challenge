import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from scr.database.connection import get_db
from scr.database.models import NQueensSolution
from scr.api.schemas import NQueensRequest, NQueensSolutionsWithCount
from scr.services.nqueens import n_queens
from scr.config.settings import settings

router = APIRouter()

@router.get("/version")
async def root():
    return {"version": "1.0"}

#end point to calculate the n queens puzzle
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
def get_or_create_solutions(request: NQueensRequest, db: Session = Depends(get_db)):
    #Validation for n greater or equal than 8
    if request.n < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="n must be greater or equal than 8"
        )

    # Search solutions in DB
    existing_solutions = db.query(NQueensSolution).filter(
        NQueensSolution.n == request.n
    ).all()

    # if there are solutions, retrieve from the DB
    if existing_solutions:
        if request.show_solutions:
            return NQueensSolutionsWithCount(
                solutions=existing_solutions,
                comments="Data retrieved from DB",
                total_solutions=len(existing_solutions)
            )
        return NQueensSolutionsWithCount(
            solutions=[],
            comments="Data retrieved from DB",
            total_solutions=len(existing_solutions)
        )


    # If no solutions exist, calculate solutions
    # Store solutions in the BD
    start_time = time.time()
    db_solutions = []
    #Calculate the solutions for n queens
    for sol in n_queens(request.n, 0, 0, 0, 0):
        #Send HTTP exception if the elapsed time has been exceeded the configured timeout period
        if abs(time.time() - start_time) > settings.TIME_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail=f"The {settings.TIME_LIMIT} seconds has been exceeded. 'n' must be less"
            )
        db_solutions.append(NQueensSolution(n=request.n, solution=list(sol)))
    time_taken = time.time() - start_time
    db.add_all(db_solutions)
    db.commit()

    length_solutions = len(db_solutions)

    #Don't show solutions when the request show_solutions is false
    if not request.show_solutions:
        db_solutions.clear()

    return NQueensSolutionsWithCount(
        comments=f"Data calculated successfully in {round(time_taken,2)} seconds",
        total_solutions=length_solutions,
        solutions=db_solutions
    )
