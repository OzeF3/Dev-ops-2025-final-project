FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy CLI source and requirements
COPY sawectl/sawectl.py /app/sawectl.py
COPY sawectl/requirements.txt /app/requirements.txt
COPY sawectl/dsl.schema.json /app/dsl.schema.json
COPY sawectl/module.schema.json /app/module.schema.json

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make CLI executable
RUN chmod +x /app/sawectl.py

# Default command
ENTRYPOINT ["python3", "/app/sawectl.py"]




