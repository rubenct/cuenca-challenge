from fastapi.testclient import TestClient
from starlette import status

from scr.main import app
from scr.config.settings import settings

client = TestClient(app)

def test_solutions():
    response = client.post(
        f"{settings.API_V1_STR}/nqueens",
        json={"n": 8, "show_solutions": True},
    )
    assert response.status_code == status.HTTP_200_OK
    jason_response = response.json()
    solutions = jason_response["solutions"]

    assert jason_response["total_solutions"] == 92

    expect_solution_8 = [3,6,2,7,1,4,0,5]
    solution_found = any(solution["solution"] == expect_solution_8 for solution in solutions)
    assert solution_found, f"Solution {expect_solution_8} not found in solutions"
