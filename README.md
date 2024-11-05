# N-Queens Solver API

This is a FastAPI-based API for solving and storing solutions to the N-Queens problem.

## Features

- Solves the N-Queens problem for an `n` value, the limit of n, is the time it takes to calculate the algorithm. It is set to 10 minutes 
- Stores the solutions in a PostgreSQL database
- Retrieves existing solutions or calculates new ones as needed
- Provides a RESTful API for interacting with the solution data

## Technologies Used

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pytest

## Getting Started
```
git clone https://github.com/rubenct/cuenca-challenge/tree/master
```

Navigate inside the repository folder and execute:

```
docker-compose up --build
```

## Available endpoints
### N queen solution puzzle
```
curl --location 'http://127.0.0.1:8080/api/v1/nqueens' \
--header 'Content-Type: application/json' \
--data '{
    "n": 8,
    "show_solutions":false
}'
```

### Healthcheck endpoint

```
curl --location --request GET 'http://127.0.0.1:8080/api/v1/version'
```
- `n` [int]: n number of queens and size of board n x n: n >= 8
- `show_solutions` [bool]: **true**: Show all solutions found (the bigger is 'n' the longer it'll take the request duration, **false**: solutions will be hidden and only show the number of solutions.


### Testing
The testing is executed once the docker service is up.
Performs a test to the **.../queens** endpoint to verify response:
- HTTP_200_OK for n valid
- That the solutions found for n=8 are 92.
- That one of the solutions for n=8 is within the solutions ([3,6,2,7,1,4,0,5])
