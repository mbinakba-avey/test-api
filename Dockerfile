FROM python:3.12-slim-bookworm

# e.g., using a hash from a previous release
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

# Copy dependencies first
COPY uv.lock pyproject.toml ./

# Create virtual environment using uv and install packages
RUN uv sync


# Copy the rest of the application code
COPY app/ app/
COPY test.db ./

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app using uvicorn via uv
CMD ["uv", "run", "-m", "app.main", "--host", "0.0.0.0", "--port", "8000"]