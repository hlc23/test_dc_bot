# ── Builder stage ────────────────────────────────────────────────────────────
# Install build tools and compile all Python dependencies into /install.
# This layer (and gcc/build-essential) will NOT be present in the final image.
FROM python:3.13-slim AS builder

WORKDIR /app

COPY ./requirements.txt /app/

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# ── Final stage ───────────────────────────────────────────────────────────────
# Clean runtime image – no build tools, only the pre-built packages.
FROM python:3.13-slim

WORKDIR /app

# Copy compiled packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY ./cogs /app/cogs
COPY ./core /app/core
# COPY ./data /app/data # mount data volume instead of copying
COPY ./utils /app/utils
COPY ./main.py /app/

# Run the bot
CMD ["python", "main.py"]
