# INSTALL.md

## Prerequisites

- Python 3.13+ (3.11-3.14 supported; 3.13/3.14 are fully tested)
- [uv](https://docs.astral.sh/uv/) — never `poetry` or bare `pip install`

## Installation Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/pkuppens/templify.git
    cd templify
    ```

2. Install dependencies using uv:
    ```sh
    uv sync --group dev
    ```

3. Run commands inside the environment:
    ```sh
    uv run <command>
    ```

## Running the Project

1. Run the project locally:
    ```sh
    uv run python -m templify
    ```

2. Run tests using `pytest`:
    ```sh
    uv run pytest
    ```

## Docker Setup

1. Build the Docker container:
    ```sh
    docker build -t templify .
    ```

2. Run the Docker container:
    ```sh
    docker run -it --rm templify
    ```

3. Use `docker-compose` to set up the environment:
    ```sh
    docker-compose up
    ```

## Additional Information

See the [Home](index.md) for more information about the project.
- [DEVELOP.md](DEVELOP.md)
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
