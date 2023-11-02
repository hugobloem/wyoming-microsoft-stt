FROM ghcr.io/home-assistant/amd64-base-debian:bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Microsoft-stt
WORKDIR /usr/src

COPY setup.py ./pkg/
COPY requirements.txt ./pkg/
ADD ./wyoming-microsoft-stt ./pkg/wyoming-microsoft-stt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat-traditional \
        curl \
        python3 \
        python3-pip \
    && pip install --no-cache-dir \
        setuptools \
        wheel \
    && pip install ./pkg \
    && rm -rf /var/lib/apt/lists/*

# Copy files
WORKDIR /
COPY rootfs /

HEALTHCHECK --start-period=10m \
    CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10300 \
        | grep -q "microsoft" \
        || exit 1
