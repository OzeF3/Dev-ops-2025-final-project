from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import requests
import subprocess
import os
import base64

app = Flask(__name__)

def clean(s):
    return ''.join(c for c in (s or '') if ord(c) < 128).strip()

# Config from environment variables
GMAIL_USER = clean(os.environ.get("GMAIL_USER", ""))
GMAIL_PASSWORD = clean(os.environ.get("GMAIL_PASSWORD", ""))
JIRA_BASE_URL = clean(os.environ.get("JIRA_BASE_URL", "https://oefraty.atlassian.net"))
JIRA_EMAIL = clean(os.environ.get("JIRA_EMAIL", "oefraty@gmail.com"))
JIRA_TOKEN = clean(os.environ.get("JIRA_TOKEN", ""))
JIRA_PROJECT = clean(os.environ.get("JIRA_PROJECT", "SEY"))
GITHUB_TOKEN = clean(os.environ.get("GITHUB_TOKEN", ""))
GITHUB_REPO = clean(os.environ.get("GITHUB_REPO", "OzeF3/Dev-ops-2025-final-project"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json
    to = clean(data.get("to"))
    subject = clean(data.get("subject"))
    body = clean(data.get("body"))

    if not all([to, subject, body]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = GMAIL_USER
        msg["To"] = to
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to, msg.as_string())

        return jsonify({"status": "ok", "message": f"Email sent to {to}"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/create-jira", methods=["POST"])
def create_jira():
    data = request.json
    summary = clean(data.get("summary"))
    description = clean(data.get("description"))
    issue_type = clean(data.get("issue_type", "Task"))

    if not all([summary, description]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        credentials = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_TOKEN}".encode()).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        }
        payload = {
            "fields": {
                "project": {"key": JIRA_PROJECT},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
                },
                "issuetype": {"name": issue_type}
            }
        }
        response = requests.post(
            f"{JIRA_BASE_URL}/rest/api/3/issue",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        issue_key = response.json().get("key")
        return jsonify({"status": "ok", "message": f"Jira issue {issue_key} created", "key": issue_key})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/save-to-git", methods=["POST"])
def save_to_git():
    data = request.json
    file_path = clean(data.get("file_path"))
    content = clean(data.get("content"))
    commit_message = clean(data.get("commit_message", "Update from Seyoawe Release App"))

    if not all([file_path, content]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
        check = requests.get(url, headers=headers)
        sha = check.json().get("sha") if check.status_code == 200 else None

        payload = {
            "message": commit_message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()

        return jsonify({"status": "ok", "message": f"File {file_path} saved to GitHub"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/run-command", methods=["POST"])
def run_command():
    data = request.json
    command = clean(data.get("command"))

    if not command:
        return jsonify({"status": "error", "message": "Missing command"}), 400

    allowed = ["ls", "pwd", "echo", "date", "whoami", "uname", "df", "free", "uptime"]
    cmd_name = command.strip().split()[0]
    if cmd_name not in allowed:
        return jsonify({"status": "error", "message": f"Command '{cmd_name}' not allowed. Allowed: {', '.join(allowed)}"}), 400

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )
        output = result.stdout or result.stderr
        return jsonify({"status": "ok", "message": "Command executed", "output": output})

    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Command timed out"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
