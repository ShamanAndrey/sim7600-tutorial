"""
Main entry point for sim7600 toolkit.
Handles subcommand dispatching for SMS, GPS, and Voice features.
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="SIM7600 Toolkit - SMS, GPS, and Voice for SIM7600G-H modem",
        epilog="Use 'python -m sim7600 <command> --help' for more information on a specific command."
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # SMS subcommand
    sms_parser = subparsers.add_parser("sms", help="SMS operations")
    sms_subparsers = sms_parser.add_subparsers(dest="sms_command", help="SMS actions")
    
    # SMS receive subcommand
    receive_parser = sms_subparsers.add_parser("receive", help="Receive and log SMS messages")
    receive_parser.add_argument("--port", default="auto", help="Serial port (e.g., COM10) or 'auto' to auto-detect")
    receive_parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    receive_parser.add_argument("--logfile", default="logs/sms.log", help="Path to log file")
    receive_parser.add_argument("--json-out", default="", help="Write messages as JSON Lines")
    receive_parser.add_argument("--no-console", action="store_true", help="Don't print messages to console")
    receive_parser.add_argument("--init-only", action="store_true", help="Initialize modem and exit")
    receive_parser.add_argument("--echo", action="store_true", help="Echo raw serial lines (debug)")
    
    # SMS send subcommand (placeholder for future)
    send_parser = sms_subparsers.add_parser("send", help="Send an SMS message (coming soon)")
    send_parser.add_argument("recipient", help="Phone number to send to")
    send_parser.add_argument("message", help="Message text to send")
    
    # GPS subcommand (placeholder for future)
    gps_parser = subparsers.add_parser("gps", help="GPS operations (coming soon)")
    gps_subparsers = gps_parser.add_subparsers(dest="gps_command", help="GPS actions")
    track_parser = gps_subparsers.add_parser("track", help="Track GPS location (coming soon)")
    track_parser.add_argument("--interval", type=int, default=5, help="Update interval in seconds")
    
    # Voice subcommand (placeholder for future)
    voice_parser = subparsers.add_parser("voice", help="Voice operations (coming soon)")
    voice_subparsers = voice_parser.add_subparsers(dest="voice_command", help="Voice actions")
    dial_parser = voice_subparsers.add_parser("dial", help="Make a phone call (coming soon)")
    dial_parser.add_argument("number", help="Phone number to call")
    
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
            print("📤 SMS sending feature coming soon!")
            print(f"Will send: '{args.message}' to {args.recipient}")
            sys.exit(1)
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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
