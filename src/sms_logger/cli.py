from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
from dotenv import load_dotenv
from .logger_config import setup_logging
from .modem import Modem, find_sim7600_port
from .parser import parse_cmt_header


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Receive and log SMS from SIM7600 (+CMT push mode)."
    )
    parser.add_argument(
        "--port",
        default=os.getenv("PORT", "auto"),
        help="Serial port (e.g., COM10) or 'auto' to auto-detect SIM7600",
    )
    parser.add_argument("--baud", type=int, default=int(os.getenv("BAUD", "115200")))
    parser.add_argument("--logfile", default=os.getenv("LOG_PATH", "logs/sms.log"))
    parser.add_argument("--json-out", default=os.getenv("JSONL_PATH", ""))
    parser.add_argument("--no-console", action="store_true")
    parser.add_argument(
        "--init-only", action="store_true", help="Send init AT commands and exit."
    )
    parser.add_argument(
        "--echo", action="store_true", help="Echo raw serial lines to console (debug)."
    )
    args = parser.parse_args()

    logger = setup_logging(
        args.logfile if args.logfile else None, console=not args.no_console
    )

    # Auto-detect port if needed
    port = args.port
    if port.lower() == "auto":
        logger.info("Auto-detecting SIM7600 modem...")
        detected_port = find_sim7600_port()
        if detected_port:
            port = detected_port
            logger.info(f"Found SIM7600 modem on {port}")
        else:
            logger.error(
                "Could not auto-detect SIM7600 modem. Please specify --port manually."
            )
            sys.exit(1)
    else:
        logger.info(f"Using specified port: {port}")

    json_path = None
    jf = None
    if args.json_out:
        json_path = Path(args.json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        jf = open(json_path, "a", encoding="utf-8")

    modem = Modem(port, args.baud, echo_raw=args.echo)
    try:
        modem.open()
    except Exception as e:
        logger.error(f"Failed to open serial port {port}: {e}")
        sys.exit(1)

    try:
        modem.init_sms_push()
        logger.info("Modem initialized for SMS push (+CMT).")

        if args.init_only:
            logger.info("Init-only requested; exiting.")
            return

        pending_header = None
        for line in modem.lines():
            if not line:
                continue

            if pending_header is None:
                hdr = parse_cmt_header(line)
                if hdr:
                    pending_header = hdr
                continue
            else:
                # The next non-empty line after +CMT header is the message body
                body = line.strip()
                if not body:
                    # Sometimes an empty line appears; keep waiting
                    continue

                message = {
                    "sender": pending_header["number"],
                    "timestamp": pending_header["timestamp"],
                    "text": body,
                    "raw_header": pending_header["raw_header"],
                }
                logger.info(
                    f'SMS from {message["sender"]} @ {message["timestamp"]}: {message["text"]}'
                )

                if jf:
                    jf.write(json.dumps(message, ensure_ascii=False) + "\n")
                    jf.flush()

                pending_header = None

    except KeyboardInterrupt:
        logger.info("Stopped by user (Ctrl+C).")
    finally:
        if jf:
            jf.close()
        modem.close()


if __name__ == "__main__":
    main()
