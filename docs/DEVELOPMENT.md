# 🛠️ Development Guide

This guide will help you understand the project structure and show you how to add new features.

## 📁 Project Structure

```
sim7600-tutorial/
├── src/
│   └── sim7600/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Entry point for `python -m sms_logger`
│       ├── cli.py               # Command-line interface & main logic
│       ├── modem.py             # Serial communication with modem
│       ├── parser.py            # Parse SMS messages from modem
│       └── logger_config.py     # Logging configuration
├── logs/                        # Generated log files (gitignored)
├── .env                         # Your local config (gitignored)
├── .env.example                 # Template for configuration
├── pyproject.toml               # Project metadata & dependencies
├── requirements.txt             # Python dependencies
└── README.md                    # User documentation
```

## 🧩 How Each Module Works

### 1. `modem.py` - Talking to the Hardware

This module handles all communication with the SIM7600 modem.

**Key components:**

- `find_sim7600_port()` - Auto-detects the modem's AT PORT
- `Modem` class - Manages serial connection and AT commands

**Example: Adding a new AT command**

```python
# In modem.py

def get_signal_strength(self) -> int:
    """Get signal strength (0-31, 99=unknown)"""
    self.write_cmd("AT+CSQ")

    # Read response lines
    for _ in range(10):  # Try up to 10 lines
        line = self.readline()
        if line.startswith("+CSQ:"):
            # Parse: +CSQ: 20,0
            parts = line.split(":")
            if len(parts) > 1:
                rssi = parts[1].split(",")[0].strip()
                return int(rssi)

    return 99  # Unknown
```

Then use it in `cli.py`:

```python
signal = modem.get_signal_strength()
logger.info(f"Signal strength: {signal}")
```

### 2. `parser.py` - Understanding SMS Messages

Parses the `+CMT:` lines from the modem into structured data.

**Example: Adding support for different SMS encodings**

```python
# In parser.py

def parse_cmt_header(line: str) -> dict | None:
    """Parse +CMT header and determine encoding"""
    if not line.startswith("+CMT:"):
        return None

    # Existing parsing...
    result = {
        "number": number,
        "timestamp": timestamp,
        "raw_header": line,
        "encoding": "GSM",  # Add encoding detection
    }

    # Check if it's a UCS2 message
    if "UCS2" in line:
        result["encoding"] = "UCS2"

    return result
```

### 3. `cli.py` - The Main Program Flow

This is where everything comes together.

**Flow:**

1. Parse command-line arguments
2. Set up logging
3. Auto-detect or use specified port
4. Open modem connection
5. Initialize modem with AT commands
6. Loop: Read lines and parse SMS messages
7. Log messages and save to files

### 4. `logger_config.py` - Logging Setup

Configures Python's logging system with file rotation.

## 🚀 Adding New Features

### Feature 1: Send SMS Messages

**Step 1:** Add sending capability to `modem.py`

```python
# In modem.py

def send_sms(self, phone_number: str, message: str) -> bool:
    """
    Send an SMS message.
    Returns True if successful, False otherwise.
    """
    # Set text mode
    self.write_cmd("AT+CMGF=1")
    time.sleep(0.5)

    # Start sending
    self.write_cmd(f'AT+CMGS="{phone_number}"')
    time.sleep(0.5)

    # Write message and end with Ctrl+Z (chr(26))
    if not self.ser or not self.ser.is_open:
        return False

    self.ser.write((message + chr(26)).encode("utf-8"))

    # Wait for response
    time.sleep(2)
    for _ in range(10):
        line = self.readline()
        if "OK" in line:
            return True
        if "ERROR" in line:
            return False

    return False
```

**Step 2:** Add CLI argument in `cli.py`

```python
# In cli.py, add argument
parser.add_argument("--send", metavar="NUMBER:MESSAGE",
                    help="Send an SMS: --send +1234567890:Hello")

# After modem initialization
if args.send:
    try:
        number, message = args.send.split(":", 1)
        logger.info(f"Sending SMS to {number}")
        if modem.send_sms(number, message):
            logger.info("SMS sent successfully!")
        else:
            logger.error("Failed to send SMS")
        sys.exit(0)
    except ValueError:
        logger.error("Invalid format. Use: --send +1234567890:Your message")
        sys.exit(1)
```

**Usage:**

```powershell
python -m sms_logger --send "+1234567890:Hello from Python!"
```

### Feature 2: Filter Messages by Keyword

**Step 1:** Add CLI argument

```python
# In cli.py
parser.add_argument("--filter", help="Only log messages containing this keyword")
```

**Step 2:** Add filtering logic

```python
# In the message processing loop in cli.py
if pending_header is None:
    hdr = parse_cmt_header(line)
    if hdr:
        pending_header = hdr
    continue
else:
    body = line.strip()
    if not body:
        continue

    # NEW: Filter logic
    if args.filter and args.filter.lower() not in body.lower():
        logger.debug(f"Filtered out message: {body}")
        pending_header = None
        continue

    # Rest of message processing...
```

### Feature 3: Webhook Notifications

**Step 1:** Add dependency to `pyproject.toml`

```toml
dependencies = [
    "pyserial>=3.5",
    "python-dotenv>=1.0.1",
    "requests>=2.31.0",  # Add this
]
```

**Step 2:** Create webhook module

```python
# Create new file: src/sms_logger/webhook.py

import requests
import json
from typing import Dict

def send_webhook(url: str, message: Dict) -> bool:
    """
    Send SMS data to a webhook URL.

    Args:
        url: Webhook URL
        message: SMS message data

    Returns:
        True if successful, False otherwise
    """
    try:
        payload = {
            "sender": message["sender"],
            "timestamp": message["timestamp"],
            "text": message["text"],
        }

        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        return response.status_code == 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return False
```

**Step 3:** Use it in `cli.py`

```python
# In cli.py
from .webhook import send_webhook

parser.add_argument("--webhook", help="Send messages to this webhook URL")

# In message processing
if args.webhook:
    if send_webhook(args.webhook, message):
        logger.debug("Webhook sent successfully")
    else:
        logger.warning("Failed to send webhook")
```

### Feature 4: Message Database (SQLite)

**Step 1:** Create database module

```python
# Create new file: src/sms_logger/database.py

import sqlite3
from typing import Dict
from pathlib import Path

class MessageDatabase:
    def __init__(self, db_path: str = "messages.db"):
        self.db_path = db_path
        self.conn = None
        self.init_db()

    def init_db(self):
        """Create database and table if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                text TEXT NOT NULL,
                received_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def save_message(self, message: Dict):
        """Save a message to the database"""
        self.conn.execute(
            "INSERT INTO messages (sender, timestamp, text) VALUES (?, ?, ?)",
            (message["sender"], message["timestamp"], message["text"])
        )
        self.conn.commit()

    def get_messages(self, sender: str = None, limit: int = 100):
        """Retrieve messages, optionally filtered by sender"""
        query = "SELECT * FROM messages"
        params = []

        if sender:
            query += " WHERE sender = ?"
            params.append(sender)

        query += " ORDER BY received_at DESC LIMIT ?"
        params.append(limit)

        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
```

**Step 2:** Use it in `cli.py`

```python
# In cli.py
from .database import MessageDatabase

parser.add_argument("--database", default="", help="Save messages to SQLite database")

# After argument parsing
db = None
if args.database:
    db = MessageDatabase(args.database)
    logger.info(f"Using database: {args.database}")

# In message processing
if db:
    db.save_message(message)

# In cleanup (finally block)
if db:
    db.close()
```

### Feature 5: Desktop Notifications (Windows)

**Step 1:** Add dependency

```toml
dependencies = [
    "pyserial>=3.5",
    "python-dotenv>=1.0.1",
    "win10toast>=0.9",  # Add this for Windows notifications
]
```

**Step 2:** Use it in `cli.py`

```python
# In cli.py
from win10toast import ToastNotifier

parser.add_argument("--notify", action="store_true",
                    help="Show Windows notifications for new SMS")

# Initialize
toaster = None
if args.notify:
    toaster = ToastNotifier()
    logger.info("Desktop notifications enabled")

# In message processing
if toaster:
    toaster.show_toast(
        f"SMS from {message['sender']}",
        message['text'],
        duration=10,
        threaded=True
    )
```

## 🧪 Testing Your Changes

### Manual Testing

1. **Test with --init-only first:**

   ```powershell
   python -m sms_logger --init-only
   ```

2. **Test your feature:**

   ```powershell
   python -m sms_logger --your-new-flag
   ```

3. **Send yourself a test SMS**

### Debug Mode

Use the `--echo` flag to see raw modem communication:

```powershell
python -m sms_logger --echo
```

### Adding Automated Tests

Create `tests/test_parser.py`:

```python
import pytest
from sim7600.parser import parse_cmt_header

def test_parse_cmt_header():
    line = '+CMT: "+1234567890","","25/10/18,14:30:00+00"'
    result = parse_cmt_header(line)

    assert result is not None
    assert result["number"] == "+1234567890"
    assert "25/10/18,14:30:00" in result["timestamp"]

def test_invalid_header():
    result = parse_cmt_header("Invalid line")
    assert result is None
```

Run with:

```powershell
pip install pytest
pytest tests/
```

## 📦 Adding Dependencies

1. **Update `pyproject.toml`:**

   ```toml
   dependencies = [
       "pyserial>=3.5",
       "python-dotenv>=1.0.1",
       "your-new-package>=1.0.0",
   ]
   ```

2. **Update `requirements.txt`:**

   ```
   pyserial>=3.5
   python-dotenv>=1.0.1
   your-new-package>=1.0.0
   ```

3. **Reinstall:**
   ```powershell
   pip install -e .
   ```

## 🎨 Code Style

- Use type hints: `def function(arg: str) -> bool:`
- Follow PEP 8 naming conventions
- Add docstrings to functions
- Keep functions focused and small
- Use meaningful variable names

## 🐛 Debugging Tips

### 1. Check Modem Responses

Add debug logging:

```python
logger.debug(f"Modem response: {line}")
```

### 2. Test AT Commands Manually

Use a serial terminal (like PuTTY) to test AT commands directly:

- Connect to the AT PORT
- Type: `AT` (should respond "OK")
- Type: `AT+CMGF=1` (set text mode)
- Type: `AT+CMGS="+1234567890"` (send SMS)

### 3. Log Everything

Add verbose logging during development:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Useful AT Commands

| Command     | What it does               |
| ----------- | -------------------------- |
| `AT`        | Test if modem responds     |
| `AT+CSQ`    | Check signal quality       |
| `AT+CREG?`  | Check network registration |
| `AT+CMGF=1` | Set text mode              |
| `AT+CMGS`   | Send SMS                   |
| `AT+CMGL`   | List stored SMS            |
| `AT+CMGD`   | Delete SMS                 |
| `AT+CPIN?`  | Check SIM card status      |

## 🔄 Contributing Your Features

1. **Fork the repository** on GitHub
2. **Create a branch**: `git checkout -b feature/my-awesome-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: `git commit -am "Add awesome feature"`
6. **Push**: `git push origin feature/my-awesome-feature`
7. **Create Pull Request** on GitHub

## 💡 Feature Ideas

### Easy

- Add message counter (show total received)
- Add time-based filtering (only log messages during certain hours)
- Colorize console output by sender
- Add sound notification when SMS arrives

### Medium

- Web dashboard to view messages
- Auto-reply bot (keyword-based responses)
- Message forwarding to email/Telegram
- Statistics dashboard (charts, graphs)

### Advanced

- Support multiple modems simultaneously
- Build REST API server
- Integration with home automation (Home Assistant, etc.)
- SMS-based command & control system

## 📖 Learning Resources

- [PySerial Documentation](https://pyserial.readthedocs.io/)
- [AT Commands Reference](https://www.developershome.com/sms/atCommandsIntro.asp)
- [SIM7600 AT Command Manual](https://www.simcom.com/product/SIM7600X.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 📦 Adding More Packages

Want to add another package alongside `sms_logger` (e.g., a web dashboard, API server, or tools)?

See **[ADDING_PACKAGES.md](ADDING_PACKAGES.md)** for a complete guide on:

- Creating multiple packages in your project
- Building a web dashboard (`sms_dashboard`)
- Creating a REST API (`sms_api`)
- Adding CLI tools (`sms_tools`)
- Sharing code between packages
- Running multiple services together

## 🆘 Need Help?

- 💬 Open a [GitHub Discussion](https://github.com/YOUR_USERNAME/sim7600-tutorial/discussions)
- 🐛 Report bugs as [Issues](https://github.com/YOUR_USERNAME/sim7600-tutorial/issues)
- 📧 Check existing issues for solutions

Happy coding! 🚀
