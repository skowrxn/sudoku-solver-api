# SuSaaS — Sudoku Solver as a Service

This project aims to produce a solver for the general [sudoku puzzle](https://en.wikipedia.org/wiki/Sudoku). The general variant is basically the sudoku with no specific size. Classically, the sudoku uses `9`x`9` grid, but in general it can any size divisible into equal blocks, e.g., `4`x`4`, `16`x`16`, `25`x`25`, etc.

This time we will run our solver as a service :)

Sources:
- [fast-api — the web framework we will use](https://fastapi.tiangolo.com/)
- [pydantic — fast-api friendly alternative to dataclasses](https://docs.pydantic.dev/latest/)

## TODO: 

There are several tasks to complete:
- [ ] copy already implemented methods from the previous lab
- [ ] implement:
    - `src/model/grid.py` — additional validation of the sudoku grid in the `post init` method
    - `src/model/requests.py` — validation of the requests made to the service
    - `src/utils/all_different.py` — a utility function to check whether an array has unique elements
    - `src/solvers/sat_solver.py` — checking whether sudoku has a unique solution using SAT
    - `api.py` - handling various requests
- [ ] use `api.py` to run your service locally
    - check the swagger
- [ ] use `render.com` to run your service public
    - instructions will be available in few minutes
- [ ] keep your code tidy by running `ruff format` and `ruff check` or using vs code `ruff` extension
    - bobot won't give points if your file is not well formatted 


## Grading

* [ ] Make sure, you have a **private** group
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [ ] Fork this project into your private group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)
* [ ] Add @bobot-is-a-bot as the new project's member (role: **maintainer**)
  * [how to add an user](https://docs.gitlab.com/ee/user/project/members/index.html#add-a-user)

## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Solve the exercises
    * use WebIDE, whatever
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to the gitlab master branch
    ```bash
    git push 
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file appears.

## Project Structure

    .
    ├── puzzles                     # contains puzzles of various sizes
    ├── src                         # source directory
    │   ├── model                   # - directory with the problem model 
    │   │   └── grid.py             # representation of the sudoku grid
    │   ├── solvers                 # TODO: directory with the sudoku solvers
    │   └── utils                   # TODO: various utilities              
    ├── benchmark.py                # you may use this script to compare solvers
    ├── main.py                     # TODO: create this file with `uv init`
    ├── pyproject.toml              # TODO: create this file with `uv init`
    └── README.md                   # the README you are reading now
