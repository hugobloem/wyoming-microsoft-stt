FROM python:3.13-slim-bullseye

# Install the Python package
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir .

EXPOSE 10300

ENTRYPOINT [ "python", "-m", "wyoming_microsoft_stt"]