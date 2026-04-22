# ============================================================================
# SeyoAWE Release App - Dockerfile
#
# Small Flask app exposing 4 release-automation functions:
#   1. POST /send-email    - Send email via Gmail SMTP
#   2. POST /create-jira   - Create a Jira issue
#   3. POST /save-to-git   - Commit a file to GitHub
#   4. POST /run-command   - Run a whitelisted shell command
#
# Built from release_app/. Consumed by the release ZIP via docker-compose.
# ============================================================================

FROM python:3.11-slim

# Non-root user for the app
RUN groupadd -r release && useradd -r -g release release

WORKDIR /app

# Install dependencies first (better layer caching)
COPY release_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY release_app/app.py .
COPY release_app/templates/ ./templates/

# Flask runs on 5000 by default in app.py
EXPOSE 5000

# Drop privileges
USER release

# Run
CMD ["python", "app.py"]
