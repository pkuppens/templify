# Use a slim Python 3.12 base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Poetry and typical dev needs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        build-essential \
        libffi-dev \
        libpq-dev \
        curl \
        git \
        && rm -rf /var/lib/apt/lists/*

# Add non-root user 'templify'
RUN useradd -ms /bin/bash templify

# Install Poetry using pip and add to PATH
RUN pip install --upgrade pip && \
    pip install poetry && \
    ln -s /usr/local/bin/poetry /usr/bin/poetry

# Copy all project files first (needed for poetry install)
COPY . .

# Install all dependencies and create virtual environment
RUN poetry config virtualenvs.create true && \
    poetry install

# Fix permissions so 'templify' user owns project files
RUN chown -R templify:templify /app

# Switch to non-root user for runtime
USER templify

# Start an interactive shell
ENTRYPOINT ["/bin/bash"]
CMD ["-l"]

# Build and run commands (for reference):
# Build the image:
#   docker build -t templify:latest .
#
# Run the container (with --rm for automatic removal on exit):
#   docker run -it --rm --name templify templify:latest
#
# Stop and remove the container (if not using --rm):
#   docker stop templify && docker rm templify
#
# Restart with new image:
#   docker run -it --rm --name templify templify:latest
