# SMS Encoding - Important Note

## ✅ What Works Today

The SMS send feature is fully functional with the SIM7600 modem using **GSM 7‑bit encoding in text mode** (`AT+CMGF=1`). This is the most compatible and reliable way to send messages.

## 📝 Character Encoding: What You Can Send

### Sends Immediately (Text Mode, GSM 7‑bit)

```powershell
python -m sim7600 sms send "+123" "Hello World 123!"
python -m sim7600 sms send "+123" "Status: OK! Temperature @ 25C."
```

### Important Limitations in Text Mode

- Non‑GSM characters (e.g., Chinese, Arabic, Cyrillic) are **not supported** for sending in text mode.
- Emoji are **not supported**.
- Accented Latin letters may be simplified/converted or replaced depending on the recipient’s handset.

See `docs/SMS_CHARACTER_LIMITS.md` for exact limits and details.

## 🔧 Why GSM‑Only for Sending

On SIM7600:

- **Text mode (AT+CMGF=1)** is simple and reliable but does **not** support sending Unicode (UCS2) messages.
- Attempting to use `AT+CSCS="UCS2"` to send in text mode results in `+CMS ERROR: Invalid text mode parameter`.
- **PDU mode (AT+CMGF=0)** is required to send Unicode; in PDU you set `DCS=0x08` (UCS2) and build the full PDU.

Our implementation uses **GSM 7‑bit** in text mode for maximum compatibility.

## 📏 Character Limits (Summary)

- Single SMS (GSM 7‑bit): **160** chars
- Concatenated (GSM 7‑bit): **153** chars/part
- Single SMS (UCS2/Unicode): **70** chars (requires PDU mode)
- Concatenated (UCS2): **67** chars/part (requires PDU mode)

Details: `docs/SMS_CHARACTER_LIMITS.md`.

## 💡 Best Practices in Text Mode

- Prefer ASCII where possible.
- Avoid emoji and non‑GSM characters.
- Keep messages under 160 characters to avoid splitting.

Examples:

```powershell
# Good (ASCII only)
python -m sim7600 sms send "+123" "Server backup completed at 3:45 PM"

# Avoid (will not send as intended in text mode)
python -m sim7600 sms send "+123" "你好 世界"
python -m sim7600 sms send "+123" "Congrats! 🎉"
```

## 📦 Need Unicode?

Use **PDU mode (AT+CMGF=0)** and set **DCS=0x08 (UCS2)** in the PDU. This enables sending Chinese, Arabic, Cyrillic, and other Unicode scripts. Implementing PDU adds complexity (address encoding, DCS, UDH for long messages), but it’s the standards‑compliant path for Unicode SMS.
