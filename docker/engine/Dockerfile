FROM ubuntu:22.04

# what i cahnged:
    ## EXPOSE 5000 -> EXPOSE 8080
    ## CMD ["/app/run.sh"] → CMD ["/app/seyoawe"]

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

# Expose the correct engine port
EXPOSE 8080

# Start the engine directly
CMD ["/app/seyoawe"]