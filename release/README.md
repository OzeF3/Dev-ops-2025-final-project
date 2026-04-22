# SeyoAWE Release App

A small Flask application that exposes **4 release-automation functions** behind a simple web UI.

## What it does

| Endpoint | Method | Purpose |
|---|---|---|
| `/send-email` | POST | Send an email via Gmail SMTP |
| `/create-jira` | POST | Create a Jira issue |
| `/save-to-git` | POST | Commit a file to a GitHub repo |
| `/run-command` | POST | Run a whitelisted shell command (ls, pwd, echo, date, whoami, uname, df, free, uptime) |

There is also a root page `/` with buttons for each function.

## Prerequisites

- Docker (with Compose plugin) - https://docs.docker.com/get-docker/

## Quick Start

1. **Configure credentials.** Copy the example env file and fill it in:

   ```bash
   cp .env.example .env
   # edit .env with your own values
   ```

2. **Start the app:**

   ```bash
   docker compose up -d
   ```

3. **Use it.** Open http://localhost:5000 in your browser, or hit the endpoints directly:

   ```bash
   # Send an email
   curl -X POST http://localhost:5000/send-email \
     -H "Content-Type: application/json" \
     -d '{"to":"someone@example.com","subject":"Hello","body":"Test"}'

   # Create a Jira issue
   curl -X POST http://localhost:5000/create-jira \
     -H "Content-Type: application/json" \
     -d '{"summary":"Release v1.0.0","description":"Automated release","issue_type":"Task"}'

   # Commit a file to GitHub
   curl -X POST http://localhost:5000/save-to-git \
     -H "Content-Type: application/json" \
     -d '{"file_path":"releases/v1.0.0.txt","content":"Released on 2026-04-22","commit_message":"Release v1.0.0"}'

   # Run a command
   curl -X POST http://localhost:5000/run-command \
     -H "Content-Type: application/json" \
     -d '{"command":"uname -a"}'
   ```

4. **Stop it:**

   ```bash
   docker compose down
   ```

## Security notes

- `.env` is git-ignored. Do not commit it.
- Gmail: use an **App Password**, not your real account password.
- Jira/GitHub: use tokens with minimum necessary scope.
- `/run-command` is whitelisted to 9 safe commands. It is not a shell endpoint.

## Troubleshooting

**Port 5000 already in use** - change `"5000:5000"` in `docker-compose.yml` to `"5001:5000"` and browse to http://localhost:5001 instead.

**Gmail "less secure apps" error** - you need an App Password. Regular Gmail passwords no longer work for SMTP.

**Jira 401** - double-check `JIRA_EMAIL` and `JIRA_TOKEN`, and that the project key exists.

**GitHub 404** - `GITHUB_REPO` must be in `owner/name` format; token needs `contents:write`.
