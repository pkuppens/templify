# DEVELOP.md

## Setting Up the Development Environment

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

## Running Tests and Code Quality Checks

1. Run tests using `pytest`:
    ```sh
    pytest
    ```

2. Run code formatting checks using `black`:
    ```sh
    black --check .
    ```

3. Run linting checks using `ruff` and `flake8`:
    ```sh
    ruff .
    flake8 .
    ```

## Contributing to the Project

1. Fork the repository on GitHub.

2. Create a new branch for your feature or bugfix:
    ```sh
    git checkout -b my-feature-branch
    ```

3. Make your changes and commit them with a clear and concise message:
    ```sh
    git add .
    git commit -m "Add new feature"
    ```

4. Push your changes to your forked repository:
    ```sh
    git push origin my-feature-branch
    ```

5. Create a pull request on the main repository and describe your changes in detail.

## Additional Information

- [README.md](README.md)
- [INSTALL.md](INSTALL.md)
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
