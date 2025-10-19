# 📱 SMS Send Feature - Usage Examples

## ✅ Feature Status

**SMS Sending is now IMPLEMENTED!** 🎉

## Basic Usage

### Send a Simple SMS

```powershell
python -m sim7600 sms send "+1234567890" "Hello from sim7600!"
```

This sends immediately with no prompts for standard ASCII text.

### Send with Auto-Detection

The modem will be automatically detected:

```powershell
python -m sim7600 sms send "+491234567890" "Test message"
```

### Specify Port Manually

```powershell
python -m sim7600 sms send "+1234567890" "Hello" --port COM10
```

### Messages with Special Characters

When your message contains special characters (accents, emoji, etc.), you'll see a confirmation prompt:

```powershell
python -m sim7600 sms send "+1234567890" "café résumé 🎉"
```

**Output:**

```
⚠️  WARNING: Your message contains special characters (accents, emoji, etc.)
The SIM7600 modem has limited support for these characters.
Your message may appear corrupted or garbled on the recipient's phone.

Original message: café résumé 🎉
May be sent as:     cafe resume ?

Do you want to continue anyway? (y/N):
```

- Type `y` to send anyway
- Type `N` or press Enter to cancel

## Character Encoding Support

### How It Works

The SIM7600 modem uses **GSM 7-bit encoding** which supports:

- ✅ Standard ASCII (A-Z, 0-9, basic punctuation)
- ⚠️ Accented characters (converted to ASCII: café → cafe)
- ❌ Emoji (replaced with ?: 🎉 → ?)

### Standard ASCII Messages

These send immediately without any prompts:

```powershell
# Perfect - no special characters
python -m sim7600 sms send "+1234567890" "Hello World"
python -m sim7600 sms send "+1234567890" "Server backup completed at 3:45 PM"
python -m sim7600 sms send "+1234567890" "Temperature: 25C, Status: OK"
```

### Messages with Special Characters

These will show a confirmation prompt before sending:

```powershell
# Has accents - shows warning
python -m sim7600 sms send "+1234567890" "Café résumé"

# Has emoji - shows warning
python -m sim7600 sms send "+1234567890" "Hello 👋"

# Mixed - shows warning
python -m sim7600 sms send "+1234567890" "¡Hola! ¿Cómo estás?"
```

**What happens:**

- Accents are removed: `café` → `cafe`
- Emoji become `?`: `👋` → `?`
- Special symbols become `?`: `¡` → `?`

## Debug Mode

See raw modem responses for troubleshooting:

```powershell
python -m sim7600 sms send "+1234567890" "Test" --echo
```

This will show:

- AT commands sent
- Modem responses
- Error messages
- Encoding decisions

## Complete Options

```powershell
python -m sim7600 sms send <recipient> <message> [options]

Options:
  --port PORT           Serial port (default: auto-detect)
  --baud RATE          Baud rate (default: 115200)
  --encoding TYPE      Encoding: auto, gsm, or ucs2 (default: auto)
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

# Send SMS with emoji (auto-detects encoding)
modem.send_sms("+1234567890", "Hello 🎉", encoding="auto")

# Force Unicode encoding
modem.send_sms("+1234567890", "Héllo Wörld!", encoding="ucs2")

# Close connection
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

### Send Alert with Special Characters

```powershell
python -m sim7600 sms send "+1234567890" "⚠️ Temperature alert: 45°C"
```

### Multiple Languages

```powershell
# French
python -m sim7600 sms send "+33123456789" "Bonjour! Ça va?"

# German
python -m sim7600 sms send "+49123456789" "Hallo! Wie geht's?"

# Spanish
python -m sim7600 sms send "+34123456789" "¡Hola! ¿Qué tal?"

# Russian
python -m sim7600 sms send "+7123456789" "Привет! Как дела?"
```

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
        send_alert("+1234567890", f"⚠️ High temperature: {temperature}°C")
```

## Troubleshooting

### Message Not Sending?

1. **Check signal strength** - Make sure antenna is connected
2. **Verify phone number** - Use international format (+1234567890)
3. **Enable debug mode** - Use `--echo` flag to see modem responses
4. **Try another port** - Manually specify with `--port COM10`

### Special Characters Garbled?

1. **Use auto encoding** (default) - Automatically detects and uses correct encoding
2. **Force UCS2** - Use `--encoding ucs2` for Unicode support
3. **Check message** - Ensure your terminal supports Unicode

### "No module named sim7600"?

Reinstall the package:

```powershell
pip install -e .
```

## Testing Checklist

Before using in production:

- [ ] Test with your own phone number
- [ ] Test with standard ASCII message
- [ ] Test with emojis/special characters
- [ ] Test with long message
- [ ] Test error handling (invalid number)
- [ ] Verify messages are received correctly

## What's Next?

Now that you can send SMS, consider building:

- **Alert System** - Send notifications from your applications
- **Auto-responder** - Reply to received messages automatically
- **Bulk SMS** - Send to multiple recipients
- **Scheduled Messages** - Send at specific times
- **SMS Gateway** - Build an API for your services

See `docs/DEVELOPMENT.md` for ideas on extending functionality!
