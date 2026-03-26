FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the engine binary
COPY seyoawe.linux /app/seyoawe
RUN chmod +x /app/seyoawe

# Copy modules and configuration
COPY modules/ /app/modules/
COPY configuration/ /app/configuration/
COPY workflows/ /app/workflows/

# Copy run script
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Expose the engine port (adjust if needed)
EXPOSE 5000

# Start the engine
CMD ["/app/run.sh"]