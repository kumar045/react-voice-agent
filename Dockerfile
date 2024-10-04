# Use the official Python image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory for the entire build process
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY server/pyproject.toml ./
COPY server/uv.lock ./

# Install dependencies
RUN pip install --no-cache-dir poetry && poetry install --no-root --no-dev

# Install `uv` for running the server
RUN pip install uv

# Copy the entire project to the working directory
COPY . .

# Change working directory to server
WORKDIR /app/server

# Expose port 3000
EXPOSE 3000

# Command to run the application
CMD ["uv", "run", "src/server/app.py"]
