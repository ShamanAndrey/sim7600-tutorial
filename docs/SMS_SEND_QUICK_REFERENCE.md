# 📱 SMS Send - Quick Reference Card

## Basic Command

```powershell
python -m sim7600 sms send "+1234567890" "Your message here"
```

## Common Options

| Option            | Description        | Example                                                     |
| ----------------- | ------------------ | ----------------------------------------------------------- |
| `--port COM10`    | Specify port       | `python -m sim7600 sms send "+123" "Hi" --port COM10`       |
| `--encoding gsm`  | Force GSM encoding | `python -m sim7600 sms send "+123" "Hi" --encoding gsm`     |
| `--encoding ucs2` | Force Unicode      | `python -m sim7600 sms send "+123" "Hi 🎉" --encoding ucs2` |
| `--echo`          | Debug mode         | `python -m sim7600 sms send "+123" "Hi" --echo`             |

## Character Encoding

| Character Type    | Behavior                           | Confirmation? |
| ----------------- | ---------------------------------- | ------------- |
| ASCII (a-z, 0-9)  | Sends perfectly                    | No            |
| Accents (é, ñ, ü) | Converted to base letter (e, n, u) | Yes           |
| Emoji (🎉, 👋)    | Replaced with `?`                  | Yes           |
| Special (¡, ¿, €) | Replaced with `?` or removed       | Yes           |
| Non-Latin scripts | May not display correctly          | Yes           |

**Note:** GSM 7-bit encoding is always used. The `--encoding` flag is informational only.

## Examples

### Standard Message (No Prompt)

```powershell
python -m sim7600 sms send "+1234567890" "Hello World!"
# Sends immediately - ASCII only
```

### With Emoji (Shows Confirmation)

```powershell
python -m sim7600 sms send "+1234567890" "Hello 👋 Test 🎉"
# Shows warning: "Hello ? Test ?" - asks for confirmation
```

### Special Characters (Shows Confirmation)

```powershell
python -m sim7600 sms send "+1234567890" "Héllo Wörld! Ça va?"
# Shows warning: "Hello World! Ca va?" - asks for confirmation
```

### Debug Mode

```powershell
python -m sim7600 sms send "+1234567890" "Test" --echo
```

### Specific Port

```powershell
python -m sim7600 sms send "+1234567890" "Test" --port COM10
```

## Python Library

```python
from sim7600 import Modem, find_sim7600_port

# Setup
port = find_sim7600_port()
modem = Modem(port)
modem.open()

# Send
modem.send_sms("+1234567890", "Hello!")

# Close
modem.close()
```

## Troubleshooting

| Problem            | Solution                                       |
| ------------------ | ---------------------------------------------- |
| "Modem not found"  | Run with `--port COM10` (check Device Manager) |
| "Failed to send"   | Try `--echo` to see modem responses            |
| Garbled characters | Use `--encoding ucs2`                          |
| Port in use        | Close other programs using the port            |

## Help Commands

```powershell
# General help
python -m sim7600 --help

# SMS help
python -m sim7600 sms --help

# Send help
python -m sim7600 sms send --help
```

## Test Your Setup

```powershell
# 1. Test modem connection
python -m sim7600 sms receive --init-only

# 2. Send test message (use your own number!)
python -m sim7600 sms send "+YOUR_NUMBER" "Test from sim7600"

# 3. Check if message received on your phone
```

## Common Patterns

### Alert Script

```python
from sim7600 import Modem, find_sim7600_port

def alert(msg):
    m = Modem(find_sim7600_port())
    m.open()
    m.send_sms("+ADMIN", f"🚨 {msg}")
    m.close()

alert("Server backup completed!")
```

### Multiple Recipients

```python
from sim7600 import Modem, find_sim7600_port
import time

numbers = ["+1111111111", "+2222222222"]
m = Modem(find_sim7600_port())
m.open()

for num in numbers:
    m.send_sms(num, "Announcement!")
    time.sleep(1)

m.close()
```

## Remember

- ✅ Use international format: `+1234567890`
- ✅ ASCII messages send immediately (no prompts)
- ✅ Special characters trigger confirmation prompt
- ✅ Use `--echo` for debugging
- ✅ Max message length: 1600 characters
- ✅ Add delay between multiple messages
- ⚠️ Accents are removed: `café` → `cafe`
- ⚠️ Emoji become `?`: `🎉` → `?`

## Files to Read

- `USAGE_EXAMPLES.md` - Detailed examples
- `SMS_SEND_IMPLEMENTATION.md` - Technical details
- `docs/DEVELOPMENT.md` - Add more features

---

**Ready to send?** 🚀

```powershell
python -m sim7600 sms send "+YOUR_NUMBER" "Hello! 🎉"
```
