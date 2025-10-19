# 🌐 SIM7600 Web Dashboard

Modern web interface for managing SMS with your SIM7600 modem.

## ✨ Features

- 📤 **Send SMS** - User-friendly form with character counter
- 📥 **Receive SMS** - Real-time message display (auto-refresh)
- ⚠️ **Special Character Warning** - Preview how non-ASCII characters will be converted
- 🔄 **Auto-Refresh** - Messages update every 5 seconds
- 📊 **Status Indicator** - See modem connection status at a glance
- 💻 **Responsive Design** - Works on desktop and mobile

## 🚀 Quick Start

### Option 1: Via main CLI (recommended)

```powershell
python -m sim7600 dashboard
```

### Option 2: Direct launch

```powershell
python -m sim7600_dashboard
```

### Option 3: Custom host/port

```powershell
python -m sim7600_dashboard --host 0.0.0.0 --port 8000
```

## 📖 Usage

1. **Launch dashboard:**

   ```powershell
   python -m sim7600 dashboard
   ```

2. **Open browser:**

   - Dashboard opens at `http://127.0.0.1:5000`

3. **Features:**
   - **Send SMS:** Fill in phone number and message, click Send
   - **View Messages:** Auto-refreshes or click Refresh button
   - **Status:** Green = Connected, Red = Disconnected

## 🔧 Options

| Option    | Description       | Default   |
| --------- | ----------------- | --------- |
| `--host`  | Host to bind to   | 127.0.0.1 |
| `--port`  | Port to bind to   | 5000      |
| `--debug` | Enable debug mode | False     |

### Examples

```powershell
# Bind to all interfaces (accessible from network)
python -m sim7600_dashboard --host 0.0.0.0

# Custom port
python -m sim7600_dashboard --port 8080

# Debug mode
python -m sim7600_dashboard --debug
```

## 📁 Architecture

**No code duplication!** This package imports from the core `sim7600` package:

```python
from sim7600 import Modem, find_sim7600_port
from sim7600.parser import parse_cmt_header
```

### Structure

```
sim7600_dashboard/
├── __init__.py           # Package initialization
├── __main__.py           # Entry point (python -m sim7600_dashboard)
├── app.py                # Flask application
├── templates/
│   └── dashboard.html    # Main dashboard UI
└── static/
    ├── style.css         # Modern CSS styling
    └── script.js         # Interactive JavaScript
```

## 🎨 UI Features

### Modern Design

- Clean, professional interface
- Responsive layout (works on mobile)
- Color-coded status indicators
- Smooth animations

### Smart Character Handling

- Detects non-ASCII characters in real-time
- Shows preview of converted message
- Warning badge appears automatically
- Same conversion logic as CLI

### Real-time Updates

- Messages refresh every 5 seconds
- Status updates every 3 seconds
- Character counter updates as you type

## 🔌 API Endpoints

If you want to integrate with the dashboard:

| Endpoint        | Method | Description                   |
| --------------- | ------ | ----------------------------- |
| `/`             | GET    | Main dashboard page           |
| `/api/status`   | GET    | Get modem connection status   |
| `/api/messages` | GET    | Get recent messages (last 50) |
| `/api/send`     | POST   | Send an SMS message           |
| `/api/connect`  | POST   | Connect to modem              |

### Example API Usage

```python
import requests

# Send SMS via API
response = requests.post('http://localhost:5000/api/send', json={
    'phone': '+1234567890',
    'message': 'Hello from API!'
})

# Get messages
response = requests.get('http://localhost:5000/api/messages')
messages = response.json()['messages']
```

## 🛠️ Development

### Run in debug mode

```powershell
python -m sim7600_dashboard --debug
```

Debug mode enables:

- Auto-reload on code changes
- Detailed error pages
- Flask debugger

### Customize the UI

**Templates:** `src/sim7600_dashboard/templates/dashboard.html`  
**Styles:** `src/sim7600_dashboard/static/style.css`  
**Scripts:** `src/sim7600_dashboard/static/script.js`

## 🆘 Troubleshooting

### "Dashboard not installed"

```powershell
pip install -e .[dashboard]
```

### Port already in use

```powershell
# Use a different port
python -m sim7600_dashboard --port 8080
```

### Can't access from other devices

```powershell
# Bind to all interfaces
python -m sim7600_dashboard --host 0.0.0.0
```

### Modem not connecting

1. Check modem is plugged in
2. Close any other programs using the modem
3. Try manual connection from dashboard
4. Check logs in terminal

## 📊 Technical Details

### Backend: Flask 3.0+

- Lightweight Python web framework
- RESTful API design
- Background thread for SMS receiving
- JSON responses

### Frontend: Vanilla JavaScript

- No framework dependencies
- Modern ES6+ features
- Fetch API for requests
- Real-time DOM updates

### Integration

- Uses core `sim7600` package
- No code duplication
- Shares same modem code
- Same character conversion logic

## ✅ Benefits of Separate Package

1. **Clean architecture** - UI is separate from core
2. **Optional dependency** - CLI users don't need Flask
3. **No duplication** - Imports from `sim7600` package
4. **Easy to extend** - Add more UI features independently

## 🎯 Future Ideas

- 📊 Message statistics and charts
- 🔍 Search and filter messages
- 💾 Export messages to CSV/JSON
- 👥 Contact management
- 📅 Scheduled SMS sending
- 🔔 Desktop notifications
- 🌙 Dark mode toggle
- 📱 PWA (Progressive Web App)

## 📚 Related Documentation

- Main project: [README.md](../../README.md)
- SMS usage: [docs/USAGE_EXAMPLES.md](../../docs/USAGE_EXAMPLES.md)
- Development: [docs/DEVELOPMENT.md](../../docs/DEVELOPMENT.md)

---

**Ready to use!** 🎉

```powershell
python -m sim7600 dashboard
```

