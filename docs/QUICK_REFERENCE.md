# 📋 SIM7600 Quick Reference

## Installation

```powershell
# With web dashboard (recommended)
pip install -e .[dashboard]

# CLI only
pip install -e .
```

## Commands

### 🌐 Web Dashboard

```powershell
python -m sim7600 dashboard                    # Start at localhost:5000
python -m sim7600 dashboard --port 8080        # Custom port
python -m sim7600 dashboard --host 0.0.0.0     # Network accessible
```

### 📤 Send SMS

```powershell
python -m sim7600 sms send "+NUMBER" "MESSAGE"           # Basic send (GSM text mode)
python -m sim7600 sms send "+NUMBER" "MESSAGE" --echo    # With debug
python -m sim7600 sms send "+NUMBER" "Cafe"               # Avoid accents/emoji in text mode
```

### 📥 Receive SMS

```powershell
python -m sim7600 sms receive                  # Start receiving
python -m sim7600 sms receive --init-only      # Test connection
python -m sim7600 sms receive --echo           # Debug mode
python -m sim7600 sms receive --no-console     # Background mode
```

## Common Options

| Option         | Description                  | Example                |
| -------------- | ---------------------------- | ---------------------- |
| `--port`       | Specify COM port             | `--port COM10`         |
| `--echo`       | Show AT commands (debug)     | `--echo`               |
| `--no-console` | Silent mode (receive only)   | `--no-console`         |
| `--init-only`  | Test and exit (receive only) | `--init-only`          |
| `--logfile`    | Custom log path (receive)    | `--logfile my.log`     |
| `--json-out`   | JSON output path (receive)   | `--json-out msg.jsonl` |

## File Locations

| File             | Description                    |
| ---------------- | ------------------------------ |
| `logs/sms.log`   | Human-readable message log     |
| `logs/sms.jsonl` | JSON format with direction tag |
| `.env`           | Configuration (optional)       |

## Message Log Format

### Received Message

```json
{
  "direction": "received",
  "sender": "+1234567890",
  "timestamp": "25/10/18,20:08:21+08",
  "text": "Hello!",
  "raw_header": "+CMT: \"+1234567890\",\"\",\"25/10/18,20:08:21+08\"",
  "received_at": "2025-10-19T04:30:00.123456"
}
```

### Sent Message

```json
{
  "direction": "sent",
  "recipient": "+1234567890",
  "text": "Hello back!",
  "timestamp": "2025-10-19T04:30:15.123456",
  "ascii_only": true
}
```

## Troubleshooting

### Modem Not Found

```powershell
# Check Device Manager for "Simcom HS-USB AT PORT"
# Look for COM port number

# Force specific port
python -m sim7600 sms receive --port COM10
```

### Port In Use

```powershell
# Kill Python processes
Get-Process python | Stop-Process -Force

# Wait 2 seconds for port to free
Start-Sleep -Seconds 2
```

### Dashboard Not Installed

```powershell
pip install -e .[dashboard]
```

### Permission Denied (PowerShell)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Character Encoding

- Text mode (`AT+CMGF=1`) sends **GSM 7‑bit only**.
- Unicode/UCS2 sending requires **PDU mode** (`AT+CMGF=0`, DCS=0x08).
- See `docs/SMS_CHARACTER_LIMITS.md` for exact limits (160/153 GSM; 70/67 UCS2).

| Character Type   | Support (Text Mode) | Behavior                     |
| ---------------- | ------------------- | ---------------------------- |
| ASCII (a-z, 0-9) | ✅ Full             | Sent as-is                   |
| GSM Extended     | ✅ Full             | Euro (€), brackets, etc.     |
| Accents (é, ñ)   | ⚠️ Converted        | é→e, ñ→n (display dependent) |
| Emoji (😀, ☕)   | ❌ Not supported    | Use PDU mode for Unicode     |

## API Endpoints (Dashboard)

| Endpoint        | Method | Purpose                        |
| --------------- | ------ | ------------------------------ |
| `/`             | GET    | Dashboard HTML                 |
| `/api/status`   | GET    | Modem connection status        |
| `/api/messages` | GET    | Recent messages (last 50)      |
| `/api/contacts` | GET    | Unique phone numbers from logs |
| `/api/send`     | POST   | Send SMS                       |

### Example API Call

```javascript
fetch("/api/send", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    phone: "+1234567890",
    message: "Hello from API!",
  }),
});
```

## Tips & Tricks

### Background Receiving

```powershell
# Run in background, log to file only
python -m sim7600 sms receive --no-console
```

### Debug AT Commands

```powershell
# See all modem communication
python -m sim7600 sms receive --echo
python -m sim7600 sms send "+123" "Test" --echo
```

### Network Access for Dashboard

```powershell
# Access from other devices on your network
python -m sim7600 dashboard --host 0.0.0.0

# Then use http://YOUR_PC_IP:5000 from other devices
```

### Test Connection Quickly

```powershell
python -m sim7600 sms receive --init-only
```

## Project Structure

```
sim7600-tutorial/
├── src/
│   ├── sim7600/              # Core package
│   │   ├── __main__.py       # CLI entry point
│   │   ├── modem.py          # Modem communication
│   │   ├── parser.py         # SMS parsing
│   │   └── logger_config.py  # Logging setup
│   └── sim7600_dashboard/    # Web UI package
│       ├── __main__.py       # Dashboard entry
│       ├── app.py            # Flask application
│       ├── templates/        # HTML templates
│       └── static/           # CSS & JavaScript
├── logs/                     # Message logs
├── docs/                     # Documentation
├── README.md                 # Main docs
├── pyproject.toml            # Package config
└── .env.example              # Config template
```

## Related Documentation

- 📖 [README.md](../README.md) - Full guide
- 📚 [SMS Character Limits](SMS_CHARACTER_LIMITS.md)
- 🌐 [Dashboard README](../src/sim7600_dashboard/README.md)
- 📚 [Usage Examples](USAGE_EXAMPLES.md)

---

**Quick Help:**

```powershell
python -m sim7600 --help              # Main help
python -m sim7600 sms --help          # SMS commands
python -m sim7600 sms send --help     # Send options
python -m sim7600 sms receive --help  # Receive options
python -m sim7600 dashboard --help    # Dashboard options
```
