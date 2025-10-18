# SMS Logger (SIM7600 / Windows)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A small, production-friendly Python project to **receive and log SMS messages** from a SIM7600 modem on Windows
using the **AT port** over a serial connection.

> ⚠️ **Note**: This project is designed for Windows. While the core functionality may work on Linux with minor modifications, it has been primarily tested on Windows.

## Features

- **Auto-detects SIM7600 modem** - no need to manually find the COM port!
- Initializes the modem (`AT+CMGF=1`, `AT+CNMI=2,2,0,0,0`) to push incoming SMS directly to the serial stream.
- Parses live `+CMT:` indications (sender, timestamp, body).
- Logs to a rotating file and optionally prints to console.
- Optional JSONL output for easy downstream processing.
- Configurable via CLI flags or a `.env` file.

## Quick Start (Windows PowerShell)

1. Install Python 3.10+ and Git.
2. Open **PowerShell** and run:
   ```powershell
   cd <your download folder>
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -e .
   ```
3. Connect your SIM7600 modem and run:
   ```powershell
   python -m sms_logger
   ```
   The program will **automatically detect** your SIM7600 modem!

### Optional Configuration

- You can still manually specify the port: `python -m sms_logger --port COM10`
- Or use a `.env` file for persistent settings:
  ```powershell
  copy .env.example .env
  notepad .env   # set PORT=auto (or COM10), BAUD=115200, LOG_PATH=logs/sms.log
  ```

## Typical AT Setup (done automatically by the app)

- `AT+CMGF=1` → text mode
- `AT+CNMI=2,2,0,0,0` → push incoming SMS (`+CMT:`) to serial immediately

## CLI

```text
usage: python -m sms_logger [-h] [--port PORT] [--baud BAUD] [--logfile LOGFILE]
                            [--json-out JSON_OUT] [--no-console] [--init-only]
                            [--echo]
```

- `--port` : serial COM port, e.g. `COM10`, or `auto` to auto-detect (default: `auto`)
- `--baud` : baud rate (default: `115200`)
- `--logfile` : path to the rotating text log file (default: `logs/sms.log`)
- `--json-out` : write structured messages as JSON Lines
- `--no-console` : do not print incoming messages to screen
- `--init-only` : just send init AT commands and exit
- `--echo` : print every raw line read from modem (debug)

## File Outputs

- **Text log** (rotating): human-readable lines with timestamps
- **JSONL**: one JSON object per line with `sender`, `timestamp`, `text`, `raw_header`

## Troubleshooting

- **Auto-detection not working?** The program looks for "Simcom" or "HS-USB AT Port" in device descriptions. You can manually specify the port with `--port COM10`.
- Make sure you have the **AT Port** showing in Device Manager (e.g., `SIMCom HS-USB AT Port (COM10)`).
- If you see nothing, confirm no other app is holding the port (close TeraTerm, Waveshare tools).
- Signal check: `AT+CSQ` (10–31 is OK). Registration: `AT+CREG?` should be `...,1` or `...,5`.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

If you encounter any issues or have suggestions, please [open an issue](https://github.com/YOUR_USERNAME/sms-logger/issues).

## Security

⚠️ **Important Security Notes:**

- Never commit your `.env` file - it may contain sensitive configuration
- The `logs/` directory contains SMS messages and phone numbers - keep it private
- This project uses `.gitignore` to prevent accidentally committing sensitive data

## Compatibility

**Tested with:**

- SIM7600 (Simcom HS-USB AT Port)
- Windows 10/11
- Python 3.10+

**May work with:**

- Other SIMCom modems with similar AT command support
- Other GSM/LTE modems (with potential modifications)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with PySerial for serial communication with AT-command compatible modems.
