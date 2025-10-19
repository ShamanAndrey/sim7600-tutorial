# SMS Character Limits and Encoding on SIM7600

## Overview

SMS over GSM has a fixed user data payload of 140 bytes per message. How many characters fit into those 140 bytes depends on the encoding used:

- GSM 7‑bit (default text mode): up to 160 characters per single SMS
- 8‑bit data: up to 140 characters
- UCS2 (16‑bit Unicode): up to 70 characters per single SMS

When messages exceed these limits, they must be split into multiple parts (concatenated SMS) using a User Data Header (UDH). The UDH itself consumes payload bytes, reducing the per‑part character capacity:

- GSM 7‑bit concatenated: 153 characters per part
- UCS2 concatenated: 67 characters per part

## Why the Limits Exist

The GSM network’s SMS transport allocates exactly 140 bytes for the message user data field. Encoding determines how many characters can fit into that payload:

- GSM 7‑bit packs characters tightly (7 bits each), enabling 160 chars in 140 bytes (1120 bits ÷ 7 = 160).
- 8‑bit uses 1 byte per character (140 chars).
- UCS2 uses 2 bytes per character (70 chars).

Additionally, some GSM 7‑bit "extended" characters (e.g., `{ } [ ] ^ | ~ \\ €`) are encoded using an escape mechanism and count as 2 characters each.

## Why This Project Uses GSM 7‑bit for Sending

On the SIM7600, sending SMS in "text mode" (AT+CMGF=1) works reliably with the GSM character set via:

```
AT+CMGF=1          // text mode
AT+CSCS="GSM"      // TE character set for text mode
AT+CMGS="+123..."  // recipient
> Hello World       // message, then Ctrl+Z
```

Attempting to send Unicode in text mode using `AT+CSCS="UCS2"` is rejected by the module for outbound messages with `+CMS ERROR: Invalid text mode parameter`. In practice, on SIM7600 the TE character set selection (`AT+CSCS`) in text mode is meant for how the terminal displays/enters characters rather than for transporting UCS2 over the air. As a result, Unicode sending in text mode is not supported.

## When You Need Other Encodings (Unicode/UCS2)

To send Unicode (e.g., Chinese, Arabic, Cyrillic, emoji), you must use **PDU mode**:

```
AT+CMGF=0          // PDU mode
AT+CMGS=<PDU_length>
> <full PDU hex with DCS=0x08 for UCS2>  // then Ctrl+Z
```

In PDU mode you explicitly build the full SMS binary:

- SMSC information
- Submit header/flags
- Address (recipient) in swapped semi‑octets
- Protocol ID
- Data Coding Scheme (set to 0x08 for UCS2)
- Optional UDH for concatenation
- User data (message) encoded accordingly (UTF‑16 BE for UCS2)

Because you control the Data Coding Scheme (DCS) in PDU, the network will transport UCS2 correctly. This is the standards‑compliant way to send non‑GSM characters.

## Practical Implications

- **Text mode (AT+CMGF=1)**: use GSM 7‑bit only. This project sends with `AT+CSCS="GSM"` for maximum compatibility. Non‑GSM characters should be avoided or transformed.
- **PDU mode (AT+CMGF=0)**: required for sending Unicode/UCS2. Implementing PDU requires:
  - 7‑bit packing (if using GSM)
  - UCS2 (UTF‑16 BE) encoding (if using Unicode)
  - Phone number semi‑octet swapping
  - Concatenation headers for long messages
  - Accurate byte/character accounting (140‑byte payload rule)

## Character Counting Cheat Sheet

Single‑part limits:

- GSM 7‑bit: 160 chars
- UCS2: 70 chars

Concatenated limits (with UDH):

- GSM 7‑bit: 153 chars/part
- UCS2: 67 chars/part

Notes for GSM 7‑bit:

- Extended characters `{ } [ ] ^ | ~ \\ €` count as 2 characters each.

## Summary

- The 140‑byte SMS payload cap defines all character limits.
- In text mode on SIM7600, only GSM 7‑bit sending is supported.
- To send Unicode, you must use PDU mode with DCS=0x08 (UCS2) and build the full PDU.
- Implementing PDU adds complexity (packing, addressing, UDH) but enables true international text support.
