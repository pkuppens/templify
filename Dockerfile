# Use a slim Python 3.13 base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for uv and typical dev needs
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

# Install uv using pip and add to PATH
RUN pip install --upgrade pip && \
    pip install uv && \
    ln -s /usr/local/bin/uv /usr/bin/uv

# Copy all project files first (needed for uv sync)
COPY . .

# Install all dependencies and create virtual environment
RUN uv sync --group dev

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
