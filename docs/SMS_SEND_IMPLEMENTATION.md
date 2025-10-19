# ✅ SMS Send Feature - Implementation

## Summary

This project implements SMS sending for SIM7600 using **text mode** (`AT+CMGF=1`) with **GSM 7‑bit encoding** for maximum compatibility. Unicode (UCS2) sending is **not supported in text mode** on SIM7600; to send Unicode you must use **PDU mode** (`AT+CMGF=0`) and set the Data Coding Scheme (DCS) to `0x08`.

## What Was Implemented

### 1. Core Functionality (`modem.py`)

- Input validation (phone number, message length)
- Text mode setup: `AT+CMGF=1`, `AT+CSCS="GSM"`
- Send sequence using `AT+CMGS` and Ctrl+Z
- Response handling (`>`, `+CMGS`, `OK`, `+CMS ERROR`)
- Debug (`--echo`) support for tracing modem I/O

### 2. CLI Integration (`__main__.py`)

- Auto‑detection of modem port
- Manual port and baud selection
- Debug flag (`--echo`)
- Clear success/error logging

### 3. Library Exports (`__init__.py`)

- `find_sim7600_port` for auto‑detecting the AT port
- `Modem` class for programmatic use

## Usage Examples

```powershell
# Basic send (GSM text mode)
python -m sim7600 sms send "+1234567890" "Hello World!"

# Debug mode (see AT dialog)
python -m sim7600 sms send "+1234567890" "Test" --echo
```

Programmatic:

```python
from sim7600 import Modem, find_sim7600_port

port = find_sim7600_port()
modem = Modem(port)
modem.open()
modem.send_sms("+1234567890", "Hello!")
modem.close()
```

## Character Encoding Details

### Text Mode (Implemented)

- Encoding: **GSM 7‑bit** only
- Single‑part limit: **160** characters
- Concatenated parts: **153** characters per part (UDH overhead)
- Some extended GSM characters `{ } [ ] ^ | ~ \\ €` count as 2 characters each
- Non‑GSM characters (e.g., Chinese/Arabic/Cyrillic/emoji) are not supported for sending in text mode

See `docs/SMS_CHARACTER_LIMITS.md` for details.

### Unicode (UCS2) Sending (Not Implemented in Text Mode)

- SIM7600 rejects UCS2 sending in text mode with `+CMS ERROR: Invalid text mode parameter`
- Proper approach is **PDU mode** (`AT+CMGF=0`) with DCS set to `0x08` and the message encoded as UTF‑16 BE in the PDU
- PDU mode requires building full PDUs (SMSC, submit header, address encoding, DCS, UDH for concatenation)

## Design Decisions

- Use text mode + GSM for simplicity and reliability
- Do not attempt Unicode sending in text mode (modem rejects it)
- Keep interface clear and predictable; document limits and trade‑offs

## Next Steps (If Unicode Is Required)

- Implement **PDU mode** for outbound SMS with:
  - Address semi‑octet encoding
  - DCS selection (0x00 for GSM 7‑bit, 0x08 for UCS2)
  - UDH support for concatenated messages
  - Accurate septet/UCS2 length calculations
- Provide helper tools for PDU assembly and debugging

## References

- `docs/SMS_CHARACTER_LIMITS.md` – Character limits and encodings
- GSM 03.38 – GSM 7‑bit alphabet and packing
- GSM 03.40 – SMS PDU format
