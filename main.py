import argparse
import pathlib
import sys
from src.solvers.solver_type import SudokuSolverType
from src.model.grid import SudokuGrid


def parse_arguments() -> argparse.Namespace:
    """
    Parses the command line arguments.
    Run `python main.py -h` to learn about them.

    Returns
    --------
    parsed_args: argparse.Namespace
        parsed arguments
    """
    arg_parser = argparse.ArgumentParser(
        prog="sudolver",
        description="Sudolver - yet another sudoku solver.",
    )
    arg_parser.add_argument(
        "--algorithm",
        "-a",
        type=SudokuSolverType,
        choices=list(SudokuSolverType),
        default=SudokuSolverType.FIRST_FAIL,
        help="algorithm used to solver the sudoku",
    )
    arg_parser.add_argument(
        "--time-limit",
        "-t",
        dest="time_limit",
        type=float,
        default=60.0,
        help="time limit for the solver (in seconds)",
    )
    arg_parser.add_argument(
        "puzzle_path",
        type=pathlib.Path,
        help="path to the file containing a sudoku puzzle",
    )
    return arg_parser.parse_args()


def get_puzzle(filepath: pathlib.Path) -> SudokuGrid:
    with open(filepath) as f:
        lines = f.readlines()
    return SudokuGrid.from_text(lines)


def main() -> int:
    args = parse_arguments()
    puzzle = get_puzzle(args.puzzle_path)

    try:
        solution = args.algorithm.solve(puzzle, args.time_limit)

        if solution is None:
            print("INFEASIBLE")
            return 1
    except TimeoutError:
        print("TIMEOUT")
        return 2

    print(solution)
    return 0


if __name__ == "__main__":
    sys.exit(main())
