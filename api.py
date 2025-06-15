from src.solvers.sat_solver import SatSudokuValidator  # noqa
from src.model.requests import SolveRequest, ValidateRequest
from src.model.responses import SolveResponse, ValidateResponse

import uvicorn

from fastapi import FastAPI, HTTPException  # noqa
from src.model.grid import SudokuGrid  # noqa

app = FastAPI()


@app.post("/solve", response_model=SolveResponse)
def solve_sudoku(req: SolveRequest) -> SolveResponse:
    puzzle = SudokuGrid.from_list(req.puzzle)
    time_limit = req.time_limit
    solver_type = req.solver

    try:
        result = solver_type.solve(puzzle, time_limit)
        if result is None:
            raise HTTPException(status_code=400, detail="INFEASIBLE")
        else:
            solved_as_list = result.to_list()
            return SolveResponse(solution=solved_as_list)
    except TimeoutError:
        raise HTTPException(status_code=400, detail="TIMEOUT")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # TODO:
    # Solve the problem defined in the request.
    # - build the SudokuGrid from the list representation
    #   SudokuGrid has static method `from_list` :)
    # - solve the sudoku
    #   - if succeeded return the solution as a list
    #     SudokuGrid has now a `to_list` method :)
    #     *warning*: in `SolverResponse` constructor provide the argument as a keyword argument, e.g.,
    #       `SolverResponse(solution=...)`
    #   - in case the solver failed to find a solution:
    #     raise HTTPException with code 400 and detail "INFEASIBLE"
    #   - in case of timeout:
    #     raise HTTPException with code 400 and detail "TIMEOUT"
    #   - in case of other exceptions
    #     raise HTTPException with code 400 and detail being the exception message
    #
    # https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
    # raise NotImplementedError("not implemented yet")


@app.post("/validate", response_model=ValidateResponse)
def validate_sudoku(req: ValidateRequest) -> ValidateResponse:
    sudoku = SudokuGrid.from_list(req.puzzle)
    if SatSudokuValidator.has_unique_solution(sudoku):
        return ValidateResponse(valid=True)
    else:
        return ValidateResponse(valid=False)
    # TODO:
    # Check if the puzzle in the request is valid (has unique solution)
    # - build the SudokuGrid from the list representation
    #   SudokuGrid has static method `from_list` :)
    # - use SatSudokuValidator class to check if the puzzle has unique solution
    # - return appropriate ValidateResponse
    #   *warning*: in `ValidateResponse` constructor provide the argument as a keyword argument, e.g.,
    #       `ValidateResponse(valid=...)`
    #
    # https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
    # raise NotImplementedError("not implemented yet")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
