# 📱 SIM7600 Tutorial: SMS, GPS & Voice

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Complete toolkit for your SIM7600G-H modem!** Send and receive SMS, monitor messages in real-time with a web dashboard, and automate communications on your Windows computer! 🚀

Perfect for:

- 📱 **Send & Receive SMS** - Full two-way SMS communication
- 🌐 **Web Dashboard** - Modern UI for managing messages
- 🔔 Building SMS notification systems
- 📊 Logging messages for analysis
- 🤖 IoT and automation projects
- 🎓 Educational projects and experimenting

> 💡 **Beginner-friendly!** No prior experience needed. Just follow the steps below.

> 🪟 **Windows only** - This guide is for Windows 10/11. Linux users can adapt with minor changes.

personal note this project was mostly created using AI and I'm using SIM7600g-H 4G HAT (b) for the development of this repository. If you find any issues with your setup please raise and issue.

## 🛠️ What You'll Need

Before you start, make sure you have:

1. **SIM7600G-H Modem** (or compatible SIMCom modem)

   - USB cable to connect to your computer
   - Active SIM card inserted into the modem
   - Antenna connected (important for signal!)

2. **Windows Computer** (Windows 10 or 11)
3. **Python 3.10 or newer**
   - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ During installation, check "Add Python to PATH"!

That's it! Everything else will be installed automatically.

## ✨ What This Does

### 📥 SMS Receiving

- **Automatically finds your modem** - no manual port configuration!
- **Receives SMS in real-time** - messages appear as they arrive
- **Logs everything** - saves to text files and JSON format
- **Shows messages on screen** - see incoming SMS instantly

### 📤 SMS Sending

- **Send SMS from CLI** - Quick command-line sending
- **Character encoding support** - Handles special characters and accents
- **User-friendly warnings** - Preview message before sending

### 🌐 Web Dashboard

- **Modern web interface** - Send and view messages in your browser
- **Real-time updates** - Messages refresh automatically
- **Phone number autocomplete** - Quick access to your contacts
- **Minimal, clean design** - Focused on usability
- **Message history** - View sent and received messages

![SIM7600 SMS Dashboard](docs/dashboard_image.png)

### 🔧 Developer-Friendly

- **Easy to use** - just run one command!
- **No code duplication** - Modular package architecture
- **Full logging** - Debug with detailed logs
- **Thread-safe** - Concurrent sending and receiving

## 🚀 Quick Start Guide

### Step 1: Connect Your Modem

1. Insert your SIM card into the SIM7600G-H modem
2. Connect the antenna (📡 optional, depends on signal strength)
3. Plug the USB cable into your computer
4. Wait for Windows to install drivers (this happens automatically)
5. Check Device Manager - you should see several "Simcom HS-USB" ports

### Step 2: Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.10 or newer
3. Run the installer
4. ⚠️ **IMPORTANT**: Check the box "Add Python to PATH"
5. Click "Install Now"

### Step 3: Download This Project

Open **PowerShell** (search for it in Windows Start menu) and run:

```powershell
cd Downloads
git clone https://github.com/YOUR_USERNAME/sim7600-tutorial.git
cd sim7600-tutorial
```

> **Don't have Git?** Download the ZIP from GitHub and extract it, then `cd` to that folder.

### Step 4: Install the Program

In PowerShell, run these commands:

```powershell
# Create a virtual environment (keeps things clean)
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install with web dashboard (recommended)
pip install -e .[dashboard]

# Or install CLI only (no web interface)
# pip install -e .
```

> 💡 You should see `(.venv)` at the start of your PowerShell prompt now.
>
> 🌐 The `[dashboard]` option installs Flask for the web interface. Skip it if you only need CLI.

### Step 5: Test Your Modem

Let's check if everything works:

```powershell
python -m sim7600 sms receive --init-only
```

You should see:

```
[INFO] Auto-detecting SIM7600 modem...
[INFO] Found SIM7600 modem on COM10
[INFO] Modem initialized for SMS push (+CMT).
[INFO] Init-only requested; exiting.
```

🎉 **Success!** Your modem is ready!

### Step 6: Start Receiving SMS

Now run the program without the `--init-only` flag:

```powershell
python -m sim7600 sms receive
```

**That's it!** The program is now running and waiting for SMS messages. Send a text to your SIM card's number and watch it appear on screen! 📱✨

Press `Ctrl+C` to stop the program.

## 🎮 Usage Guide

### 🌐 Web Dashboard (Recommended)

The easiest way to use the toolkit - a modern web interface!

```powershell
python -m sim7600 dashboard
```

Then open `http://127.0.0.1:5000` in your browser.

**Features:**

- 📤 Send SMS with one click
- 📥 View all received messages
- ⚡ Real-time updates every 5 seconds
- 🔍 Phone number autocomplete
- ⚠️ Character encoding warnings
- 📊 Message history (sent & received)

Press `Ctrl+C` to stop.

### 📤 Send SMS from CLI

Send a quick SMS from the command line:

```powershell
# Basic usage
python -m sim7600 sms send "+1234567890" "Hello from SIM7600!"

# With debug output
python -m sim7600 sms send "+1234567890" "Test message" --echo
```

**Features:**

- ✅ Auto-detects modem
- ⚠️ Warns about special characters
- 🔄 Shows preview of converted message
- 📝 Confirmation prompt for non-ASCII text

### 📥 Receive SMS

Continuous SMS monitoring:

```powershell
# Default: shows messages on screen + logs to file
python -m sim7600 sms receive

# Silent mode (background operation)
python -m sim7600 sms receive --no-console

# With debug output
python -m sim7600 sms receive --echo
```

### 📊 View Your Messages

All messages are automatically saved to:

- `logs/sms.log` - Easy to read text format
- `logs/sms.jsonl` - JSON format (with direction: sent/received)

Open them with Notepad or any text editor!

### Run in Background

Want it to run 24/7? Use:

```powershell
python -m sim7600 sms receive --no-console
```

### Save to JSON

Track messages in JSON format:

```powershell
python -m sim7600 sms receive --json-out logs/messages.jsonl
```

### Custom Configuration

Create a `.env` file for persistent settings:

```powershell
copy .env.example .env
notepad .env
```

Edit values like:

- `PORT=auto` (or specific port like COM10)
- `LOG_PATH=logs/sms.log`
- `JSONL_PATH=logs/sms.jsonl`

## 📋 Feature Status

### ✅ Implemented

- **SMS Receiving** - Real-time message monitoring
- **SMS Sending** - CLI and web dashboard
- **Web Dashboard** - Modern UI for messaging
- **Message Logging** - Text and JSON formats
- **Auto-detection** - Finds modem automatically
- **Character Encoding** - Smart handling of special characters

### 🚧 Coming Soon

```powershell
# GPS
python -m sim7600 gps track            # Track GPS location

# Voice
python -m sim7600 voice dial "+123"    # Make phone calls
```

## 📝 Command Reference

### Web Dashboard

```powershell
python -m sim7600 dashboard              # Launch web interface
python -m sim7600 dashboard --port 8080  # Custom port
python -m sim7600 dashboard --host 0.0.0.0  # Allow network access
```

### SMS Receiving

```powershell
python -m sim7600 sms receive              # Start receiving SMS
python -m sim7600 sms receive --init-only  # Just test connection
python -m sim7600 sms receive --echo       # Debug mode
```

**Options:**

| Option         | Description                                 | Example                     |
| -------------- | ------------------------------------------- | --------------------------- |
| `--port`       | Specify COM port (auto-detected by default) | `--port COM10`              |
| `--logfile`    | Where to save messages                      | `--logfile my_sms.log`      |
| `--json-out`   | Save as JSON too                            | `--json-out messages.jsonl` |
| `--no-console` | Don't show messages on screen (silent mode) | `--no-console`              |
| `--init-only`  | Test connection and exit                    | `--init-only`               |
| `--echo`       | Show raw modem responses (debugging)        | `--echo`                    |

### SMS Sending

```powershell
python -m sim7600 sms send "+1234567890" "Your message"
python -m sim7600 sms send "+1234567890" "Test" --echo  # Debug mode
```

**Options:**

| Option       | Description                      | Example          |
| ------------ | -------------------------------- | ---------------- |
| `--port`     | Specify COM port                 | `--port COM10`   |
| `--echo`     | Show raw modem responses         | `--echo`         |
| `--encoding` | Force encoding (auto, gsm, ucs2) | `--encoding gsm` |

### Examples

```powershell
# Web dashboard (easiest!)
python -m sim7600 dashboard

# Receive SMS continuously
python -m sim7600 sms receive

# Send a quick SMS
python -m sim7600 sms send "+1234567890" "Hello!"

# Send with special characters (will show preview)
python -m sim7600 sms send "+1234567890" "Café ☕"

# Silent background receiving
python -m sim7600 sms receive --no-console

# Custom log location
python -m sim7600 sms receive --logfile C:\MyLogs\sms.log

# Debug mode (see AT commands)
python -m sim7600 sms receive --echo
python -m sim7600 sms send "+123" "Test" --echo
```

## 🔧 Troubleshooting

### "Could not find SIM7600 modem"

**Check these:**

1. Is the modem plugged in via USB?
2. Open Device Manager (search in Start menu)
3. Look for "Ports (COM & LPT)"
4. You should see multiple "Simcom HS-USB" devices
5. One should say "AT PORT" - that's what we need!

**If you don't see any Simcom devices:**

- Unplug and replug the USB cable
- Try a different USB port
- Check if Windows is installing drivers (bottom-right notification area)
- Restart your computer

### "Port COM10 is already in use"

Someone else is using the COM port! Try this:

```powershell
# Find what's using the port
Get-Process python* | Where-Object {$_.ProcessName -like "*python*"}

# Kill it (replace 12345 with the actual Process ID)
Stop-Process -Id 12345 -Force
```

Or just:

- Close any serial terminal programs (TeraTerm, PuTTY, Arduino IDE)
- Restart your computer (easiest!)

### "Python is not recognized"

You forgot to add Python to PATH during installation!

**Fix:**

1. Uninstall Python (Windows Settings → Apps)
2. Download from [python.org](https://www.python.org/downloads/) again
3. Run installer
4. ⚠️ **CHECK "Add Python to PATH"**
5. Install

### "Not receiving any SMS"

**Check your modem status:**

```powershell
# Test connection
python -m sim7600 sms receive --init-only
```

**Check signal strength:**

- Make sure the antenna is connected
- The modem should have a blinking LED
- Try moving to a window or outside

**Check SIM card:**

- Is it inserted correctly?
- Is it activated by your carrier?
- Can you send SMS to this number from another phone?

### "Permission denied" or ".venv\Scripts\Activate.ps1 cannot be loaded"

PowerShell security settings are blocking the script.

**Fix:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating the virtual environment again.

### Dashboard Issues

**"Dashboard not installed" or "No module named sim7600_dashboard"**

```powershell
pip install -e .[dashboard]
```

**Can't access dashboard from another computer**

```powershell
# Allow network access (default is localhost only)
python -m sim7600 dashboard --host 0.0.0.0
```

**Dashboard stuck on "Sending..." button**

Make sure you're running the latest code:

```powershell
Ctrl+C  # Stop dashboard
python -m sim7600 dashboard  # Restart
```

**"Failed to send SMS" in dashboard but CLI works**

The modem might be in use. Check:

1. Close the CLI receiver if it's running
2. Check terminal output for error messages
3. Try restarting the dashboard

### Still having issues?

1. **Check Device Manager**: You should see "Simcom HS-USB AT PORT 9001 (COM10)" or similar
2. **Multiple ports?**: The SIM7600 creates 5 different COM ports - the program auto-selects the right one (AT PORT)
3. **Manual port**: If auto-detection fails, manually specify: `python -m sim7600 sms receive --port COM10`
4. **Enable debug mode**: Run with `--echo` to see raw modem communication
5. **Open an issue**: [Report a bug on GitHub](https://github.com/YOUR_USERNAME/sim7600-tutorial/issues)

## 💡 Project Ideas

Now that you can receive SMS, here are some cool things you could build:

### Beginner Projects

- 📊 **SMS Stats Dashboard** - Count messages by sender, time of day
- 🔔 **Desktop Notifications** - Pop up a notification when SMS arrives
- 📧 **SMS to Email** - Forward messages to your email address
- 📝 **Keyword Logger** - Only save messages containing specific words

### Intermediate Projects

- 🤖 **Auto-Responder** - Send automatic replies (add sending capability)
- 📱 **Multi-SIM Manager** - Run multiple modems simultaneously
- 🔐 **2FA Code Extractor** - Parse and display verification codes
- 📈 **Analytics Dashboard** - Web interface showing message statistics

### Advanced Projects

- 🏠 **Home Automation** - Control devices via SMS commands
- 🚨 **Security System** - Get alerts from sensors via SMS
- 🌐 **SMS API Server** - Build a REST API for SMS integration
- 📡 **IoT Gateway** - Bridge between SMS and IoT devices

**Share your projects!** Open a discussion on GitHub to show what you built!

## 🤝 Contributing & Development

Want to add features or modify the code?

- 🛠️ **[Development Guide](DEVELOPMENT.md)** - Learn how to add features and modify the code
- 🐛 [Report bugs](https://github.com/YOUR_USERNAME/sim7600-tutorial/issues)
- 💡 [Suggest features](https://github.com/YOUR_USERNAME/sim7600-tutorial/issues)
- 🔧 [Submit pull requests](CONTRIBUTING.md)

We welcome contributions from beginners! Don't be shy - everyone's first contribution counts.

**Popular feature additions:**

- Sending SMS messages
- Webhook notifications
- Database storage
- Desktop notifications
- Message filtering

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed guides on implementing these!

## 🔒 Security & Privacy

⚠️ **Important Notes:**

- Your `.env` file may contain sensitive settings - never share it
- The `logs/` folder contains phone numbers and messages - keep it private!
- This project uses `.gitignore` to protect your data automatically
- For production use, add encryption and access controls

## 📚 Documentation

### Quick Reference

- **[README.md](README.md)** - You're here! Quick start and usage guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project

### Developer Guides

- **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Add features and understand the code
- **[docs/ADDING_PACKAGES.md](docs/ADDING_PACKAGES.md)** - Create multi-package projects
- **[docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** - High-level architecture explanation
- **[docs/ARCHITECTURE_DECISIONS.md](docs/ARCHITECTURE_DECISIONS.md)** - Design rationale and choices

### SMS Send Feature

- **[docs/USAGE_EXAMPLES.md](docs/USAGE_EXAMPLES.md)** - Detailed SMS send usage examples
- **[docs/SMS_SEND_QUICK_REFERENCE.md](docs/SMS_SEND_QUICK_REFERENCE.md)** - Quick command reference
- **[docs/SMS_SEND_IMPLEMENTATION.md](docs/SMS_SEND_IMPLEMENTATION.md)** - Technical implementation details
- **[docs/SMS_ENCODING_NOTE.md](docs/SMS_ENCODING_NOTE.md)** - Character encoding explained
- **[docs/SMS_SEND_FEATURE_COMPLETE.md](docs/SMS_SEND_FEATURE_COMPLETE.md)** - Complete feature summary

### Migration & Publishing

- **[docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)** - Upgrade from old `sms_logger` version
- **[docs/PUBLISH.md](docs/PUBLISH.md)** - Publishing to GitHub

## 📖 Learning Resources

Want to understand how this works? Check out:

- [AT Commands Reference](https://www.developershome.com/sms/atCommandsIntro.asp) - Learn about SMS AT commands
- [PySerial Documentation](https://pyserial.readthedocs.io/) - Serial communication in Python
- [SIM7600 Datasheet](https://www.simcom.com/product/SIM7600X.html) - Official modem documentation

## ✅ Tested With

- **Modem**: SIM7600G-H (Simcom HS-USB AT Port)
- **OS**: Windows 10 & 11
- **Python**: 3.10, 3.11, 3.12

Should also work with: SIM7600A, SIM7600E, SIM7600SA-H, and similar SIMCom modems.

## 📚 Documentation

### Core Documentation

- 📖 [README.md](README.md) - This file (getting started guide)
- 📋 [CHANGELOG.md](CHANGELOG.md) - Version history and feature updates
- 📝 [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) - Command cheat sheet

### Feature-Specific

- 🌐 [Web Dashboard Guide](src/sim7600_dashboard/README.md) - Dashboard documentation
- 📱 [Usage Examples](docs/USAGE_EXAMPLES.md) - Code examples and recipes
- 🔧 [Development Guide](docs/DEVELOPMENT.md) - For contributors

### Reference

- 🏗️ [Architecture](docs/ADDING_PACKAGES.md) - Package structure
- 📊 [AT Commands](docs/AT_COMMANDS.md) - Modem command reference (if exists)

## 📄 License

MIT License - Free to use, modify, and distribute. See [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Built with [PySerial](https://github.com/pyserial/pyserial) for serial communication
- Thanks to the SIMCom community for AT command documentation
- Special thanks to everyone who tests and improves this project!

---

**Enjoying this project?** Give it a ⭐ on GitHub and share it with others!

**Questions?** Open an issue - we're here to help! 💬
