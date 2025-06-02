import argparse
import pathlib
import sys
from src.solvers.solver_type import SudokuSolverType
from src.model.grid import SudokuGrid
from timeit import default_timer as timer


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
        "--time-limit",
        "-t",
        dest="time_limit",
        type=float,
        default=60.0,
        help="time limit for the each solver (in seconds)",
    )
    arg_parser.add_argument(
        "--repetitions",
        "-r",
        type=int,
        default=10,
        help="how many times do we repeat an experiment",
    )
    arg_parser.add_argument(
        "puzzle_paths",
        type=pathlib.Path,
        nargs="*",
        help="path to the files containing benchmark puzzles",
    )
    return arg_parser.parse_args()


def get_puzzle(filepath: pathlib.Path) -> SudokuGrid:
    with open(filepath) as f:
        lines = f.readlines()
    return SudokuGrid.from_text(lines)


def main() -> int:
    args = parse_arguments()
    puzzles = [get_puzzle(puzzle_path) for puzzle_path in args.puzzle_paths]
    results = {}

    for solver_type in SudokuSolverType:
        try:
            start = timer()
            for puzzle, _ in zip(puzzles, range(args.repetitions)):
                solution = solver_type.solve(puzzle, args.time_limit)
                if solution is None:
                    results[solver_type] = "failure"
            took = timer() - start
            average_took = took / args.repetitions
            results[solver_type] = average_took
        except TimeoutError:
            results[solver_type] = "timeout"
            continue
        except Exception:
            results[solver_type] = "failure"
            continue

    good_results = sorted(
        [
            (solver, time)
            for (solver, time) in results.items()
            if isinstance(time, float)
        ],
        key=lambda r: r[1],
    )

    bad_results = [
        (solver, msg) for (solver, msg) in results.items() if isinstance(msg, str)
    ]

    for solver, result in bad_results:
        print(f"{solver}: \t{result} sec")
    for solver, msg in good_results:
        print(f"{solver}: \t{msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
