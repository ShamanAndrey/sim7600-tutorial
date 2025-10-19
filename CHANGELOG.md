# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-10-19

### ✨ Major Features Added

#### 🌐 Web Dashboard

- **New package**: `sim7600_dashboard` - Separate web UI package
- Modern, minimal web interface for SMS management
- Real-time message updates (auto-refresh every 5 seconds)
- Send and view SMS messages in your browser
- Phone number autocomplete from message history
- Visual distinction between sent and received messages
- Thread-safe concurrent operations
- Clean, responsive design optimized for usability

**Usage:**

```powershell
python -m sim7600 dashboard
# Then open http://127.0.0.1:5000
```

#### 📤 SMS Sending

- **CLI command**: `python -m sim7600 sms send <phone> <message>`
- Auto-detection of modem (no manual port configuration needed)
- Character encoding handling:
  - GSM 7-bit encoding for ASCII characters
  - Unicode normalization for accented characters
  - User confirmation prompt for non-ASCII characters
  - Preview of how special characters will be converted
- Smart response parsing with early exit (improved performance)
- Debug mode with `--echo` flag to show AT commands

**Usage:**

```powershell
python -m sim7600 sms send "+1234567890" "Hello!"
python -m sim7600 sms send "+1234567890" "Café" --echo  # Shows preview
```

### 🔧 Improvements

#### Message Logging

- **Direction tracking**: All messages now tagged with `direction: "sent"` or `direction: "received"`
- Sent messages are logged to `logs/sms.jsonl`
- Unified log format for both sent and received messages
- In-memory message list includes sent messages (max 100 recent)

#### Performance

- **Faster SMS sending**: Early exit from response loop (~18s → ~2-3s)
- Reduced initial wait time (2s → 1s)
- Smart detection of both `+CMGS:` and `OK` responses
- Thread-safe modem access with locks

#### User Experience

- Phone number autocomplete in web dashboard
- Character count indicator
- Real-time special character warnings
- Connection status indicators
- Minimal, clean UI design
- Better error messages

### 🏗️ Architecture

#### Package Structure

- Clean separation: `sim7600` (core) + `sim7600_dashboard` (UI)
- **Zero code duplication**: Dashboard imports from core package
- Optional dashboard dependency: `pip install -e .[dashboard]`
- Professional modular architecture

#### Code Quality

- Thread-safe concurrent operations with `threading.Lock`
- Proper resource cleanup
- Consistent error handling
- Unicode support with fallbacks for Windows console

### 📚 Documentation

#### Updated

- `README.md` - Complete feature guide with examples
- Installation instructions for dashboard
- Comprehensive command reference
- Troubleshooting section for common issues
- Feature status tracker

#### New

- `src/sim7600_dashboard/README.md` - Dashboard-specific documentation
- `WEB_DASHBOARD_COMPLETE.md` - Implementation details
- API endpoint documentation

### 🐛 Bug Fixes

- Fixed SMS send hanging for 18+ seconds (early loop exit)
- Fixed Windows console Unicode encoding errors (emoji fallbacks)
- Fixed concurrent modem access issues (thread locks)
- Fixed message display not showing sent messages

### 🔒 Breaking Changes

None. All existing functionality remains backward compatible.

---

## [0.1.0] - 2024-XX-XX

### Initial Release

#### Features

- SMS receiving with real-time monitoring
- Automatic modem detection
- Message logging (text and JSON formats)
- AT command interface
- SMS parser for +CMT format
- Configurable via `.env` file
- Windows support

#### Commands

- `python -m sim7600 sms receive` - Receive SMS
- `python -m sim7600 sms receive --init-only` - Test connection

---

## Future Roadmap

### 🚧 Planned Features

#### GPS Support

- Real-time location tracking
- Location logging
- Geofence alerts

#### Voice Support

- Make phone calls
- Answer calls
- DTMF tones

#### Dashboard Enhancements

- Message search and filtering
- Export to CSV/JSON
- Contact management
- Scheduled SMS sending
- Message templates
- Dark mode
- PWA (Progressive Web App)

#### Advanced Features

- Multiple modem support
- REST API for external apps
- Webhook notifications
- SMS scheduling
- Auto-replies

---

## Installation

### Standard (CLI only)

```powershell
pip install -e .
```

### With Dashboard

```powershell
pip install -e .[dashboard]
```

## Usage

### Web Dashboard (Recommended)

```powershell
python -m sim7600 dashboard
```

### CLI

```powershell
# Receive SMS
python -m sim7600 sms receive

# Send SMS
python -m sim7600 sms send "+1234567890" "Hello!"
```

---

**Legend:**

- ✨ New features
- 🔧 Improvements
- 🐛 Bug fixes
- 🔒 Breaking changes
- 📚 Documentation
- 🏗️ Architecture
