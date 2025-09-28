FROM python:3.13-slim-bullseye

# Install the Python package
COPY . /app
WORKDIR /app
RUN uv pip install --no-cache-dir .

EXPOSE 10300

ENTRYPOINT [ "uv", "run", "-m", "wyoming_microsoft_stt"]