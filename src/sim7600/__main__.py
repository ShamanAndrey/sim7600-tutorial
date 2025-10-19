"""
Main entry point for sim7600 toolkit.
Handles subcommand dispatching for SMS, GPS, and Voice features.
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="SIM7600 Toolkit - SMS, GPS, and Voice for SIM7600G-H modem",
        epilog="Use 'python -m sim7600 <command> --help' for more information on a specific command.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # SMS subcommand
    sms_parser = subparsers.add_parser("sms", help="SMS operations")
    sms_subparsers = sms_parser.add_subparsers(dest="sms_command", help="SMS actions")

    # SMS receive subcommand
    receive_parser = sms_subparsers.add_parser(
        "receive", help="Receive and log SMS messages"
    )
    receive_parser.add_argument(
        "--port",
        default="auto",
        help="Serial port (e.g., COM10) or 'auto' to auto-detect",
    )
    receive_parser.add_argument(
        "--baud", type=int, default=115200, help="Baud rate (default: 115200)"
    )
    receive_parser.add_argument(
        "--logfile", default="logs/sms.log", help="Path to log file"
    )
    receive_parser.add_argument(
        "--json-out", default="", help="Write messages as JSON Lines"
    )
    receive_parser.add_argument(
        "--no-console", action="store_true", help="Don't print messages to console"
    )
    receive_parser.add_argument(
        "--init-only", action="store_true", help="Initialize modem and exit"
    )
    receive_parser.add_argument(
        "--echo", action="store_true", help="Echo raw serial lines (debug)"
    )

    # SMS send subcommand
    send_parser = sms_subparsers.add_parser(
        "send", help="Send an SMS message"
    )
    send_parser.add_argument("recipient", help="Phone number (e.g., +1234567890)")
    send_parser.add_argument("message", help="Message text to send")
    send_parser.add_argument(
        "--port",
        default="auto",
        help="Serial port or 'auto' to auto-detect"
    )
    send_parser.add_argument(
        "--baud", type=int, default=115200, help="Baud rate (default: 115200)"
    )
    send_parser.add_argument(
        "--encoding",
        default="auto",
        choices=["auto", "gsm", "ucs2"],
        help="Character encoding: auto (default), gsm (ASCII), ucs2 (Unicode/emoji)"
    )
    send_parser.add_argument(
        "--echo", action="store_true", help="Echo raw serial lines (debug)"
    )

    # GPS subcommand (placeholder for future)
    gps_parser = subparsers.add_parser("gps", help="GPS operations (coming soon)")
    gps_subparsers = gps_parser.add_subparsers(dest="gps_command", help="GPS actions")
    track_parser = gps_subparsers.add_parser(
        "track", help="Track GPS location (coming soon)"
    )
    track_parser.add_argument(
        "--interval", type=int, default=5, help="Update interval in seconds"
    )

    # Voice subcommand (placeholder for future)
    voice_parser = subparsers.add_parser("voice", help="Voice operations (coming soon)")
    voice_subparsers = voice_parser.add_subparsers(
        dest="voice_command", help="Voice actions"
    )
    dial_parser = voice_subparsers.add_parser(
        "dial", help="Make a phone call (coming soon)"
    )
    dial_parser.add_argument("number", help="Phone number to call")
    
    # Dashboard subcommand
    dashboard_parser = subparsers.add_parser("dashboard", help="Launch web dashboard")
    dashboard_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    dashboard_parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind to (default: 5000)"
    )
    dashboard_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    args = parser.parse_args()

    # Dispatch to appropriate handler
    if args.command == "sms":
        if args.sms_command == "receive":
            # Import and run the SMS receiver
            from .cli import main as sms_main

            # Convert args to sys.argv format for backwards compatibility
            sys.argv = ["sim7600"]
            if args.port != "auto":
                sys.argv.extend(["--port", args.port])
            if args.baud != 115200:
                sys.argv.extend(["--baud", str(args.baud)])
            if args.logfile != "logs/sms.log":
                sys.argv.extend(["--logfile", args.logfile])
            if args.json_out:
                sys.argv.extend(["--json-out", args.json_out])
            if args.no_console:
                sys.argv.append("--no-console")
            if args.init_only:
                sys.argv.append("--init-only")
            if args.echo:
                sys.argv.append("--echo")
            sms_main()
        elif args.sms_command == "send":
            # Import and initialize modem
            from .modem import Modem, find_sim7600_port
            from .logger_config import setup_logging
            
            logger = setup_logging(None, console=True)
            
            # Auto-detect or use specified port
            port = args.port
            if port.lower() == "auto":
                logger.info("Auto-detecting SIM7600 modem...")
                detected_port = find_sim7600_port()
                if detected_port:
                    port = detected_port
                    logger.info(f"Found SIM7600 modem on {port}")
                else:
                    logger.error("Could not find SIM7600 modem. Specify --port manually.")
                    sys.exit(1)
            else:
                logger.info(f"Using specified port: {port}")
            
            # Check for non-ASCII characters and warn user
            try:
                args.message.encode("ascii")
            except UnicodeEncodeError:
                # Message contains non-ASCII characters
                print("\n⚠️  WARNING: Your message contains special characters (accents, emoji, etc.)")
                print("The SIM7600 modem has limited support for these characters.")
                print("Your message may appear corrupted or garbled on the recipient's phone.")
                print(f"\nOriginal message: {args.message}")
                
                # Show what might be sent
                import unicodedata
                normalized = unicodedata.normalize('NFD', args.message)
                preview = ''
                for char in normalized:
                    if ord(char) < 128:
                        preview += char
                    elif unicodedata.category(char) == 'Mn':
                        continue
                    else:
                        preview += '?'
                print(f"May be sent as:     {preview}")
                
                response = input("\nDo you want to continue anyway? (y/N): ")
                if response.lower() != 'y':
                    logger.info("Message sending cancelled by user.")
                    sys.exit(0)
                print()  # Empty line for clarity
            
            # Open modem
            modem = Modem(port, args.baud, echo_raw=args.echo)
            try:
                modem.open()
                logger.info(f"Connected to modem on {port}")
                
                # Send SMS
                logger.info(f"Sending SMS to {args.recipient}...")
                logger.info(f"Message: {args.message}")
                if args.encoding != "auto":
                    logger.info(f"Using {args.encoding.upper()} encoding")
                
                if modem.send_sms(args.recipient, args.message, encoding=args.encoding):
                    logger.info("✅ SMS sent successfully!")
                    sys.exit(0)
                else:
                    logger.error("❌ Failed to send SMS")
                    logger.error("Try running with --echo flag to see modem responses")
                    sys.exit(1)
                    
            except ValueError as e:
                logger.error(f"Invalid input: {e}")
                sys.exit(1)
            except Exception as e:
                logger.error(f"Error: {e}")
                sys.exit(1)
            finally:
                modem.close()
        else:
            sms_parser.print_help()
    elif args.command == "gps":
        if args.gps_command == "track":
            print("📍 GPS tracking feature coming soon!")
            sys.exit(1)
        else:
            gps_parser.print_help()
    elif args.command == "voice":
        if args.voice_command == "dial":
            print("📞 Voice calling feature coming soon!")
            print(f"Will call: {args.number}")
            sys.exit(1)
        else:
            voice_parser.print_help()
    elif args.command == "dashboard":
        try:
            from sim7600_dashboard import run_dashboard
            run_dashboard(host=args.host, port=args.port, debug=args.debug)
        except ImportError:
            print("❌ Dashboard not installed!")
            print("\nTo install the dashboard, run:")
            print("  pip install -e .[dashboard]")
            print("\nOr run it directly:")
            print("  python -m sim7600_dashboard")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
