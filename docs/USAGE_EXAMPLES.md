# 📱 SMS Send Feature - Usage Examples

## ✅ Feature Status

**SMS Sending is implemented in text mode (GSM 7‑bit).**

## Basic Usage

### Send a Simple SMS

```powershell
python -m sim7600 sms send "+1234567890" "Hello from sim7600!"
```

This sends immediately with no prompts for standard ASCII text.

### Auto-Detected Modem

```powershell
python -m sim7600 sms send "+491234567890" "Test message"
```

### Specify Port Manually

```powershell
python -m sim7600 sms send "+1234567890" "Hello" --port COM10
```

### Messages with Special Characters (Text Mode)

Text mode supports GSM 7‑bit only. Accents may be simplified by handsets; emoji and non‑GSM characters are not supported in text mode.

```powershell
# Accents and symbols may not render as expected in text mode
python -m sim7600 sms send "+1234567890" "Cafe resume"
```

## Character Encoding Support (Text Mode)

### How It Works

The SIM7600 in text mode uses **GSM 7‑bit** which supports:

- ✅ Standard ASCII (A‑Z, 0‑9, basic punctuation)
- ⚠️ Accented characters (display depends on handset; prefer ASCII)
- ❌ Emoji and non‑GSM scripts (Chinese/Arabic/Cyrillic) are not supported in text mode

See `docs/SMS_CHARACTER_LIMITS.md` for limits.

### Standard ASCII Messages

These send immediately without any prompts:

```powershell
python -m sim7600 sms send "+1234567890" "Hello World"
python -m sim7600 sms send "+1234567890" "Server backup completed at 3:45 PM"
python -m sim7600 sms send "+1234567890" "Temperature: 25C, Status: OK"
```

## Debug Mode

See raw modem responses for troubleshooting:

```powershell
python -m sim7600 sms send "+1234567890" "Test" --echo
```

This will show:

- AT commands sent
- Modem responses
- Error messages

## Complete Options

```powershell
python -m sim7600 sms send <recipient> <message> [options]

Options:
  --port PORT           Serial port (default: auto-detect)
  --baud RATE          Baud rate (default: 115200)
  --echo               Show raw modem communication
```

## Using as a Python Library

You can also use the SMS send feature directly in your Python code:

```python
from sim7600 import Modem, find_sim7600_port

# Find and connect to modem
port = find_sim7600_port()
modem = Modem(port)
modem.open()

# Send SMS with standard characters
success = modem.send_sms("+1234567890", "Hello World!")
if success:
    print("✅ Message sent!")
else:
    print("❌ Failed to send")

modem.close()
```

## Error Handling

### Empty Phone Number

```powershell
python -m sim7600 sms send "" "Test"
# Error: Phone number cannot be empty
```

### Empty Message

```powershell
python -m sim7600 sms send "+1234567890" ""
# Error: Message cannot be empty
```

### Message Too Long

```powershell
python -m sim7600 sms send "+1234567890" "Very long message... (over 1600 chars)"
# Error: Message too long (max 1600 characters)
```

### Modem Not Found

```powershell
python -m sim7600 sms send "+1234567890" "Test"
# Error: Could not find SIM7600 modem. Specify --port manually.
```

## Real-World Examples

### Send Notification

```powershell
python -m sim7600 sms send "+1234567890" "Server backup completed successfully!"
```

### Multiple Languages (Text Mode Guidance)

Text mode cannot send non‑GSM scripts. Prefer transliterated ASCII when needed:

```powershell
# Prefer ASCII to ensure delivery in text mode
python -m sim7600 sms send "+33123456789" "Bonjour! Ca va?"
python -m sim7600 sms send "+49123456789" "Hallo! Wie gehts?"
python -m sim7600 sms send "+34123456789" "Hola! Que tal?"
```

> To send Chinese, Arabic, Cyrillic or emoji, use **PDU mode** (not implemented here). See `docs/SMS_CHARACTER_LIMITS.md` for details.

### Integration Example

Integrate SMS sending into your automation:

```python
import sys
from sim7600 import Modem, find_sim7600_port

def send_alert(phone: str, message: str):
    """Send SMS alert."""
    try:
        port = find_sim7600_port()
        if not port:
            print("Error: Modem not found")
            return False

        modem = Modem(port)
        modem.open()

        success = modem.send_sms(phone, message)
        modem.close()

        return success
    except Exception as e:
        print(f"Error: {e}")
        return False

# Use in your script
if __name__ == "__main__":
    # Monitor something and send alert
    temperature = 45  # Your monitoring code here

    if temperature > 40:
        send_alert("+1234567890", f"High temperature: {temperature}C")
```

## Troubleshooting

### Message Not Sending?

1. **Check signal strength** - Ensure antenna is connected
2. **Verify phone number** - Use international format (+1234567890)
3. **Enable debug mode** - Use `--echo` to see modem responses
4. **Try another port** - Manually specify with `--port COM10`

### Need Unicode (Chinese/Arabic/Cyrillic/Emoji)?

- Text mode cannot send Unicode. Implement **PDU mode** (`AT+CMGF=0`) with `DCS=0x08` (UCS2) to send international scripts.

## Testing Checklist

Before using in production:

- [ ] Test with your own phone number
- [ ] Test with standard ASCII message
- [ ] Test with long message
- [ ] Test error handling (invalid number)

## What's Next?

Now that you can send SMS, consider building:

- **Alert System** - Send notifications from your applications
- **Auto-responder** - Reply to received messages automatically
- **Bulk SMS** - Send to multiple recipients
- **Scheduled Messages** - Send at specific times
- **SMS Gateway** - Build an API for your services

See `docs/DEVELOPMENT.md` for ideas on extending functionality!
