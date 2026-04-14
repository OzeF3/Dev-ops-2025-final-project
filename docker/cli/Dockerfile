FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the built Linux binary
COPY sawectl/binaries/linux/sawectl /app/sawectl
RUN chmod +x /app/sawectl

# Copy schemas needed by the CLI
COPY sawectl/dsl.schema.json /app/dsl.schema.json
COPY sawectl/module.schema.json /app/module.schema.json

ENTRYPOINT ["/app/sawectl"]



