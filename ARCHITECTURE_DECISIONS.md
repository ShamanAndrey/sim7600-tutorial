# Architecture Decisions: Adding SMS Sending

## Decision: Keep Sending and Receiving in Same Package

### Current Structure

```
sms_logger/        # Receives SMS
```

### Proposed Structure (Recommended)

```
sms_logger/        # Both receives AND sends SMS
├── modem.py       # Core modem communication (both directions)
├── receiver.py    # Receiving-specific code (optional refactor)
├── sender.py      # Sending-specific code
├── cli.py         # CLI for receiving
└── send_cli.py    # CLI for sending (optional)
```

## Why Same Package?

### ✅ Advantages

1. **Shared Modem Connection** - Both features use the same serial connection
2. **Code Reuse** - No duplication of port detection, AT commands
3. **Simpler for Users** - One package to install and import
4. **Natural Evolution** - Easy to add sending to existing receiving code
5. **Better for Tutorial** - Keeps things simple and focused

### Example Usage:

```python
# Receiving (existing)
python -m sim7600 sms receive

# Sending (new)
python -m sim7600 sms send "+1234567890:Hello!"

# Or use as library
from sim7600 import Modem
modem = Modem()
modem.send_sms("+1234567890", "Hello from Python!")
```

## Alternative Approaches

### Option 2: Separate Packages (Not Recommended for Now)

```
src/
├── sim7600_receive/      # Receiving only
├── sim7600_send/         # Sending only
└── sim7600_common/       # Shared utilities
```

**When to use:**

- When sending and receiving have very different requirements
- When you want to package them separately for distribution
- When the codebase grows significantly (1000+ lines per package)

**Disadvantages:**

- More complex for beginners
- Code duplication or need for third package (sms_common)
- More imports: `from sms_logger import ...` AND `from sms_sender import ...`

### Option 3: Rename Package (Future Consideration)

```
src/
└── sms_manager/     # Both sending and receiving
    ├── receive.py
    └── send.py
```

**When to use:**

- If "logger" in the name becomes misleading
- When you have many SMS operations beyond just logging

**Disadvantages:**

- Breaking change for existing users
- Need to deprecate old package name

## Recommended Implementation Plan

### Phase 1: Add to Existing Package ✅ (Start Here)

1. **Add sending methods to `modem.py`:**

```python
# In modem.py
def send_sms(self, phone_number: str, message: str) -> bool:
    """Send an SMS message."""
    # Implementation...
```

2. **Optionally create `sender.py` for complex sending logic:**

```python
# In sender.py
class SMSSender:
    def __init__(self, modem: Modem):
        self.modem = modem

    def send_bulk(self, recipients: list, message: str):
        """Send to multiple recipients."""
        # Implementation...

    def send_scheduled(self, phone: str, message: str, delay: int):
        """Send after a delay."""
        # Implementation...
```

3. **Update CLI to support sending:**

```python
# In cli.py
parser.add_argument("--send", help="Send SMS: --send +123:message")
```

### Phase 2: Refactor if Needed (Later)

If the package grows too large (>1000 lines), consider:

1. **Split receiving logic into `receiver.py`:**

```python
# Move receiving code from cli.py to receiver.py
class SMSReceiver:
    def __init__(self, modem: Modem):
        self.modem = modem

    def start_listening(self, callback):
        """Start listening for SMS."""
        # Current cli.py logic here
```

2. **Create separate CLIs:**

```python
# sms_logger/__main__.py - Receiving
# sms_logger/send_cli.py - Sending with: python -m sms_logger.send
```

### Phase 3: Extract if Really Needed (Future)

Only if:

- Each package is >2000 lines
- You want separate PyPI packages
- You have multiple developers working independently

Then split into:

```
src/
├── sms_logger/      # Receiving
├── sms_sender/      # Sending
└── sms_core/        # Shared (modem, parser, etc.)
```

## Code Examples

### Simple Implementation (Recommended)

**Just add to existing `modem.py`:**

```python
class Modem:
    # ... existing methods ...

    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send an SMS message."""
        self.write_cmd("AT+CMGF=1")  # Text mode
        time.sleep(0.5)

        self.write_cmd(f'AT+CMGS="{phone_number}"')
        time.sleep(0.5)

        # Send message + Ctrl+Z
        self.ser.write((message + chr(26)).encode("utf-8"))

        # Wait for OK
        time.sleep(2)
        for _ in range(10):
            line = self.readline()
            if "OK" in line:
                return True
            if "ERROR" in line:
                return False
        return False
```

**Use in CLI:**

```python
# In cli.py
if args.send:
    phone, msg = args.send.split(":", 1)
    if modem.send_sms(phone, msg):
        logger.info("✅ SMS sent!")
    else:
        logger.error("❌ Failed to send")
    sys.exit(0)
```

### Advanced Implementation (If Needed Later)

**Create dedicated sender module:**

```python
# sender.py
from typing import List, Callable
import time
from .modem import Modem

class SMSSender:
    def __init__(self, modem: Modem):
        self.modem = modem
        self.sent_count = 0

    def send(self, phone: str, message: str) -> bool:
        """Send a single SMS."""
        result = self.modem.send_sms(phone, message)
        if result:
            self.sent_count += 1
        return result

    def send_bulk(self, recipients: List[str], message: str,
                   progress_callback: Callable = None):
        """Send to multiple recipients with progress tracking."""
        results = []
        for i, phone in enumerate(recipients):
            success = self.send(phone, message)
            results.append((phone, success))

            if progress_callback:
                progress_callback(i + 1, len(recipients), phone, success)

            time.sleep(1)  # Delay between messages

        return results

    def send_with_retry(self, phone: str, message: str,
                       max_retries: int = 3) -> bool:
        """Send with automatic retry on failure."""
        for attempt in range(max_retries):
            if self.send(phone, message):
                return True
            time.sleep(2)
        return False
```

## Project Structure Comparison

### Beginner-Friendly (Recommended for Tutorial)

```
sms_logger/
├── __init__.py       # from .modem import Modem
├── modem.py          # send_sms() method added
├── cli.py            # --send flag added
└── ...
```

**Pros:** Simple, easy to understand, minimal changes

### Intermediate (Good for Growth)

```
sms_logger/
├── __init__.py       # Export Receiver, Sender
├── modem.py          # Core modem operations
├── receiver.py       # Receiving logic
├── sender.py         # Sending logic (SMSSender class)
├── cli.py            # Receiving CLI
└── ...
```

**Pros:** Organized, scalable, clear separation

### Advanced (Only If Needed)

```
src/
├── sms_logger/       # Receiving
├── sms_sender/       # Sending
└── sms_core/         # Shared modem code
```

**Pros:** Maximum modularity
**Cons:** Complex, overkill for most use cases

## Summary

**For SIM7600G-H Tutorial:**

✅ **Start with adding to existing package**

- Add `send_sms()` method to `modem.py`
- Add `--send` flag to CLI
- Keep it simple!

📦 **Package name:** `sim7600`

- It's already established
- Name is less important than functionality
- Can always rename later if really needed

🔄 **Refactor later if:**

- Code exceeds 1000 lines
- You add many sending features (bulk, scheduled, templates)
- Users request separate packages

## Quick Start Code

Here's the minimal code to add sending:

```python
# Add this to modem.py
def send_sms(self, phone_number: str, message: str) -> bool:
    """Send an SMS message. Returns True if successful."""
    try:
        self.write_cmd("AT+CMGF=1")
        time.sleep(0.5)
        self.write_cmd(f'AT+CMGS="{phone_number}"')
        time.sleep(0.5)
        self.ser.write((message + chr(26)).encode("utf-8"))
        time.sleep(2)

        for _ in range(10):
            line = self.readline()
            if "OK" in line:
                return True
            if "ERROR" in line:
                return False
        return False
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

# Add this to cli.py
parser.add_argument("--send", metavar="PHONE:MESSAGE",
                    help="Send SMS: --send +1234567890:Hello")

# Before the main loop, add:
if args.send:
    try:
        phone, message = args.send.split(":", 1)
        logger.info(f"Sending SMS to {phone}...")
        if modem.send_sms(phone, message):
            logger.info("✅ SMS sent successfully!")
        else:
            logger.error("❌ Failed to send SMS")
        sys.exit(0)
    except ValueError:
        logger.error("Invalid format. Use: --send +1234567890:Your message")
        sys.exit(1)
```

## Conclusion

**Recommendation:** Keep it in `sms_logger` package. It's simpler, more maintainable, and better for a tutorial project. You can always refactor later if the codebase grows significantly.

The package name doesn't need to change - many packages do more than their name suggests (e.g., `requests` does both sending and receiving HTTP).
