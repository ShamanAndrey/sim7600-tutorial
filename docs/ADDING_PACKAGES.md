# Adding Additional Packages to Your Project

## When Would You Want Multiple Packages?

You might want to add another package folder when:

- Building a web dashboard → `sms_dashboard/`
- Creating an API server → `sms_api/`
- Adding utility scripts → `sms_tools/`
- Building a GUI application → `sms_gui/`
- Separating test utilities → `test_helpers/`

## Example: Adding a Web Dashboard Package

### Step 1: Create the Package Structure

Create a new folder in `src/`:

```
sim7600-tutorial/
├── src/
│   ├── sim7600/          # Your existing package
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── cli.py
│   │   ├── modem.py
│   │   ├── parser.py
│   │   └── logger_config.py
│   │
│   └── sms_dashboard/       # NEW package
│       ├── __init__.py
│       ├── __main__.py      # Entry point for `python -m sms_dashboard`
│       ├── app.py           # Flask/FastAPI app
│       └── templates/
│           └── index.html
```

### Step 2: Create the Files

**Create `src/sms_dashboard/__init__.py`:**

```python
"""Web dashboard for viewing SMS messages."""

__version__ = "0.1.0"
__all__ = ["app"]
```

**Create `src/sms_dashboard/app.py`:**

```python
from flask import Flask, render_template, jsonify
import json
from pathlib import Path

app = Flask(__name__)

def load_messages():
    """Load messages from the JSONL file"""
    messages = []
    log_path = Path("logs/sms.jsonl")

    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))

    return messages

@app.route("/")
def index():
    """Main dashboard page"""
    return render_template("index.html")

@app.route("/api/messages")
def get_messages():
    """API endpoint to get all messages"""
    messages = load_messages()
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

**Create `src/sms_dashboard/__main__.py`:**

```python
"""Entry point for running the dashboard."""

from .app import app

if __name__ == "__main__":
    print("Starting SMS Dashboard on http://localhost:5000")
    app.run(debug=True, port=5000, host="0.0.0.0")
```

**Create `src/sms_dashboard/templates/index.html`:**

```html
<!DOCTYPE html>
<html>
  <head>
    <title>SMS Dashboard</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      .message {
        border: 1px solid #ddd;
        padding: 10px;
        margin: 10px 0;
      }
      .sender {
        font-weight: bold;
        color: #007bff;
      }
      .timestamp {
        color: #666;
        font-size: 0.9em;
      }
    </style>
  </head>
  <body>
    <h1>📱 SMS Dashboard</h1>
    <div id="messages"></div>

    <script>
      async function loadMessages() {
        const response = await fetch("/api/messages");
        const messages = await response.json();

        const container = document.getElementById("messages");
        container.innerHTML = messages
          .reverse()
          .map(
            (msg) => `
                <div class="message">
                    <div class="sender">From: ${msg.sender}</div>
                    <div class="timestamp">${msg.timestamp}</div>
                    <div>${msg.text}</div>
                </div>
            `
          )
          .join("");
      }

      loadMessages();
      setInterval(loadMessages, 5000); // Refresh every 5 seconds
    </script>
  </body>
</html>
```

### Step 3: Update `pyproject.toml`

You need to tell Python about your new package:

```toml
[project]
name = "SIM7600g-H_Tutorial"
version = "0.1.0"
description = "Tutorial for SIM7600G-H: Receive and log SMS on Windows"
authors = [{name = "You"}]
requires-python = ">=3.10"
dependencies = [
    "pyserial>=3.5",
    "python-dotenv>=1.0.1",
    "flask>=3.0.0",  # Add for dashboard
]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
# This will automatically find both sms_logger and sms_dashboard
```

### Step 4: Update `requirements.txt`

Add new dependencies:

```txt
pyserial>=3.5
python-dotenv>=1.0.1
flask>=3.0.0
```

### Step 5: Reinstall the Package

```powershell
pip install -e .
```

### Step 6: Use Your New Package

Now you can run both packages:

```powershell
# Run the SMS logger (original)
python -m sms_logger

# Run the web dashboard (new)
python -m sms_dashboard
```

## Sharing Code Between Packages

Your packages can import from each other:

**In `sms_dashboard/app.py`:**

```python
# Import from the other package
from sim7600.parser import parse_cmt_header
from sim7600.modem import find_sim7600_port

# Use the functions
port = find_sim7600_port()
print(f"Found modem on: {port}")
```

**In `sim7600/cli.py`:**

```python
# You could also import from dashboard if needed
# from sms_dashboard.app import load_messages
```

## Example: Adding a CLI Tools Package

### Create `src/sms_tools/`

```
src/sms_tools/
├── __init__.py
├── __main__.py
├── stats.py        # Calculate statistics
├── export.py       # Export to different formats
└── search.py       # Search through messages
```

**`src/sms_tools/stats.py`:**

```python
"""Calculate SMS statistics."""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

def analyze_messages(log_path: str = "logs/sms.jsonl"):
    """Analyze SMS messages and show statistics."""
    messages = []

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                messages.append(json.loads(line))

    # Count by sender
    senders = Counter(msg["sender"] for msg in messages)

    print(f"\n📊 SMS Statistics")
    print(f"{'='*50}")
    print(f"Total messages: {len(messages)}")
    print(f"\nTop senders:")

    for sender, count in senders.most_common(5):
        print(f"  {sender}: {count} messages")

    return messages

if __name__ == "__main__":
    analyze_messages()
```

**`src/sms_tools/__main__.py`:**

```python
"""CLI tools for SMS analysis."""

import argparse
from .stats import analyze_messages
from .export import export_to_csv
from .search import search_messages

def main():
    parser = argparse.ArgumentParser(description="SMS Tools")
    subparsers = parser.add_subparsers(dest="command")

    # Stats command
    subparsers.add_parser("stats", help="Show statistics")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export to CSV")
    export_parser.add_argument("--output", default="messages.csv")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search messages")
    search_parser.add_argument("query", help="Search term")

    args = parser.parse_args()

    if args.command == "stats":
        analyze_messages()
    elif args.command == "export":
        export_to_csv(args.output)
    elif args.command == "search":
        search_messages(args.query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Usage:**

```powershell
# Show statistics
python -m sms_tools stats

# Export to CSV
python -m sms_tools export --output my_messages.csv

# Search messages
python -m sms_tools search "pizza"
```

## Example: Adding an API Server Package

### Create `src/sms_api/`

```
src/sms_api/
├── __init__.py
├── __main__.py
├── server.py       # FastAPI server
└── models.py       # Data models
```

**`src/sms_api/server.py`:**

```python
"""REST API for SMS access."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="SMS API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    sender: str
    timestamp: str
    text: str

def load_messages() -> List[dict]:
    """Load messages from JSONL file."""
    messages = []
    log_path = Path("logs/sms.jsonl")

    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))

    return messages

@app.get("/")
def root():
    """API root endpoint."""
    return {"message": "SMS API", "version": "1.0.0"}

@app.get("/messages", response_model=List[Message])
def get_messages(sender: Optional[str] = None, limit: int = 100):
    """Get all messages, optionally filtered by sender."""
    messages = load_messages()

    if sender:
        messages = [m for m in messages if m["sender"] == sender]

    return messages[-limit:]

@app.get("/messages/search")
def search_messages(q: str):
    """Search messages by text content."""
    messages = load_messages()
    results = [m for m in messages if q.lower() in m["text"].lower()]
    return results

@app.get("/senders")
def get_senders():
    """Get list of unique senders."""
    messages = load_messages()
    senders = list(set(m["sender"] for m in messages))
    return {"senders": senders}
```

**`src/sms_api/__main__.py`:**

```python
"""Run the API server."""

import uvicorn
from .server import app

if __name__ == "__main__":
    print("Starting SMS API on http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Add dependencies to `pyproject.toml`:**

```toml
dependencies = [
    "pyserial>=3.5",
    "python-dotenv>=1.0.1",
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
]
```

**Usage:**

```powershell
# Install new dependencies
pip install -e .

# Run the API server
python -m sms_api

# Access API docs at http://localhost:8000/docs
```

## Project Structure with Multiple Packages

Your final structure might look like:

```
sim7600-tutorial/
├── src/
│   ├── sim7600/      # Core SMS logger
│   ├── sms_dashboard/   # Web UI
│   ├── sms_api/         # REST API
│   └── sms_tools/       # CLI utilities
├── tests/
│   ├── test_logger/
│   ├── test_dashboard/
│   ├── test_api/
│   └── test_tools/
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Running Multiple Services Together

Create a launcher script `run_all.py`:

```python
"""Run all services together."""

import subprocess
import sys
from pathlib import Path

def run_service(name: str, command: list):
    """Run a service in a subprocess."""
    print(f"Starting {name}...")
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def main():
    processes = []

    try:
        # Start SMS logger
        processes.append(run_service(
            "SMS Logger",
            [sys.executable, "-m", "sms_logger"]
        ))

        # Start API server
        processes.append(run_service(
            "API Server",
            [sys.executable, "-m", "sms_api"]
        ))

        # Start dashboard
        processes.append(run_service(
            "Dashboard",
            [sys.executable, "-m", "sms_dashboard"]
        ))

        print("\n✅ All services started!")
        print("SMS Logger: Running")
        print("API Server: http://localhost:8000")
        print("Dashboard: http://localhost:5000")
        print("\nPress Ctrl+C to stop all services")

        # Wait for Ctrl+C
        for p in processes:
            p.wait()

    except KeyboardInterrupt:
        print("\n\nStopping all services...")
        for p in processes:
            p.terminate()
        print("All services stopped.")

if __name__ == "__main__":
    main()
```

**Usage:**

```powershell
python run_all.py
```

## Best Practices

1. **Keep packages focused**: Each package should have a single, clear purpose
2. **Minimize cross-dependencies**: Try not to have circular imports
3. **Share common code via utilities**: Create a `common/` package for shared functions
4. **Document each package**: Add README in each package folder
5. **Independent testing**: Each package should have its own tests

## Common Package Ideas

- `sim7600` - Core modem functionality (existing)
- `sms_sender` - SMS sending functionality
- `sms_api` - REST API server
- `sms_dashboard` - Web interface
- `sms_tools` - CLI utilities
- `sms_bot` - Auto-response bot
- `sms_forwarder` - Forward to email/Telegram
- `sms_common` - Shared utilities

## Updating Documentation

When adding packages, update your README.md:

````markdown
## Project Packages

This project consists of multiple packages:

- **sim7600** - Core SMS receiving and logging
- **sms_dashboard** - Web-based message viewer
- **sms_api** - REST API for programmatic access
- **sms_tools** - Command-line utilities

### Running Different Components

```powershell
# SMS Logger
python -m sim7600 sms receive

# Web Dashboard
python -m sms_dashboard

# API Server
python -m sms_api

# CLI Tools
python -m sms_tools stats
```
````

```

## Need Help?

If you're building something complex with multiple packages, consider:
- Reading about Python package structure
- Looking at large Python projects (Django, Flask, etc.)
- Opening a discussion on GitHub to share your architecture

Happy building! 🚀

```
