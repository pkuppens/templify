# INSTALL.md

## Prerequisites

- Python 3.12+
- Poetry

## Installation Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/pkuppens/templify.git
    cd templify
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Set up the virtual environment:
    ```sh
    poetry shell
    ```

## Running the Project

1. Run the project locally:
    ```sh
    python -m templify
    ```

2. Run tests using `pytest`:
    ```sh
    pytest
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

See the [README](README.md) for more information about the project.
- [DEVELOP.md](DEVELOP.md)
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
