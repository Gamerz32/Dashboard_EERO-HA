# Build the current dashboard source from this repository for the HAOS app.
FROM python:3.12-alpine AS builder

ARG SOURCE_REPOSITORY=https://github.com/Gamerz32/Dashboard_EERO-HA.git
ARG SOURCE_REF=main

RUN apk add --no-cache \
    git \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    zlib-dev \
    jpeg-dev

WORKDIR /source
RUN git clone --depth 1 --branch "$SOURCE_REF" "$SOURCE_REPOSITORY" .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade "pip>=26.2.0" "setuptools>=83.0.0" wheel \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine AS app

ARG APP_VERSION=1.6.2
ARG BUILD_VERSION
ARG BUILD_ARCH

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    APP_VERSION=$APP_VERSION \
    PATH="/opt/venv/bin:$PATH" \
    DATA_DIR=/data \
    HA_INGRESS_ONLY=true

LABEL io.hass.version="$BUILD_VERSION" \
      io.hass.type="app" \
      io.hass.arch="$BUILD_ARCH"

RUN apk add --no-cache \
    curl \
    tzdata \
    ca-certificates \
    libjpeg-turbo \
    zlib \
    su-exec \
    && addgroup -g 10001 -S appgroup \
    && adduser -u 10001 -S appuser -G appgroup

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /source/app/ /app/app/
COPY --from=builder /source/changelog.md /app/changelog.md
COPY --from=builder /source/README.md /app/README.md
COPY run.sh /addon/run.sh
COPY launcher.py /addon/launcher.py

RUN mkdir -p /app/data /data \
    && chown -R appuser:appgroup /app/data \
    && chmod 755 /addon/run.sh

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -fsS http://localhost:8000/api/health || exit 1

ENTRYPOINT ["/bin/sh", "/addon/run.sh"]
