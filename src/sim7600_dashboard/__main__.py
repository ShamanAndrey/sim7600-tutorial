"""
Entry point for running the web dashboard.
Usage: python -m sim7600_dashboard
"""

import argparse
from .app import run_dashboard


def main():
    parser = argparse.ArgumentParser(
        description="SIM7600 Web Dashboard - SMS management interface"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind to (default: 5000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    run_dashboard(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()


