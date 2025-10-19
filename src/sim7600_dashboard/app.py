"""
Flask web application for SIM7600 dashboard.
Uses the core sim7600 package - no code duplication!
"""

from flask import Flask, render_template, request, jsonify
from pathlib import Path
import json
import threading
from datetime import datetime
import time

# Import from core sim7600 package - no duplication!
from sim7600 import Modem, find_sim7600_port
from sim7600.parser import parse_cmt_header


app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)

# Global state
modem = None
modem_port = None
modem_connected = False
receiving_thread = None
stop_receiving = False
messages = []
modem_lock = threading.Lock()  # Prevent concurrent modem access


def load_existing_messages():
    """Load messages from the JSONL log file."""
    global messages
    log_path = Path("logs/sms.jsonl")
    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        msg = json.loads(line)
                        messages.append(msg)
                    except:
                        pass
    # Keep only last 100 messages in memory
    messages = messages[-100:]


def receive_sms_loop():
    """Background thread to receive SMS messages."""
    global modem, stop_receiving, messages

    if not modem or not modem.ser or not modem.ser.is_open:
        return

    pending_header = None
    while not stop_receiving:
        try:
            # Use lock when reading from modem
            with modem_lock:
                line = modem.readline()
            if not line:
                time.sleep(0.1)
                continue

            if pending_header is None:
                hdr = parse_cmt_header(line)
                if hdr:
                    pending_header = hdr
                continue
            else:
                body = line.strip()
                if not body:
                    continue

                message = {
                    "direction": "received",
                    "sender": pending_header["number"],
                    "timestamp": pending_header["timestamp"],
                    "text": body,
                    "raw_header": pending_header["raw_header"],
                    "received_at": datetime.now().isoformat(),
                }

                messages.append(message)
                messages[:] = messages[-100:]  # Keep last 100

                # Save to log file
                log_path = Path("logs/sms.jsonl")
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(message, ensure_ascii=False) + "\n")

                pending_header = None
        except Exception as e:
            print(f"Error in receive loop: {e}")
            time.sleep(1)


@app.route("/")
def index():
    """Main dashboard page."""
    return render_template("dashboard.html")


@app.route("/api/status")
def status():
    """Get modem connection status."""
    return jsonify(
        {
            "connected": modem_connected,
            "port": modem_port,
            "message_count": len(messages),
        }
    )


@app.route("/api/messages")
def get_messages():
    """Get recent messages."""
    # Return messages in reverse order (newest first)
    return jsonify({"messages": list(reversed(messages[-50:]))})  # Last 50 messages


@app.route("/api/contacts")
def get_contacts():
    """Get unique phone numbers from message history."""
    contacts = set()
    for msg in messages:
        if msg.get("direction") == "received" and msg.get("sender"):
            contacts.add(msg["sender"])
        elif msg.get("direction") == "sent" and msg.get("recipient"):
            contacts.add(msg["recipient"])
    return jsonify({"contacts": sorted(list(contacts))})


@app.route("/api/send", methods=["POST"])
def send_sms():
    """Send an SMS message."""
    data = request.json
    phone = data.get("phone", "").strip()
    message = data.get("message", "").strip()

    if not phone or not message:
        return jsonify({"success": False, "error": "Phone and message required"}), 400

    if not modem_connected or not modem:
        return jsonify({"success": False, "error": "Modem not connected"}), 500

    try:
        # Check for non-ASCII characters
        try:
            message.encode("ascii")
            ascii_only = True
            preview = message
        except UnicodeEncodeError:
            ascii_only = False
            # Generate preview (same logic as CLI)
            import unicodedata

            normalized = unicodedata.normalize("NFD", message)
            preview = ""
            for char in normalized:
                if ord(char) < 128:
                    preview += char
                elif unicodedata.category(char) == "Mn":
                    continue
                else:
                    preview += "?"

        # Send the message using core sim7600 package (with lock for thread safety)
        print(f"[DEBUG] Attempting to send SMS to {phone}: {message}")
        with modem_lock:
            success = modem.send_sms(phone, message)
        print(f"[DEBUG] send_sms returned: {success}")

        if success:
            # Log the sent message
            sent_message = {
                "direction": "sent",
                "recipient": phone,
                "text": message,
                "timestamp": datetime.now().isoformat(),
                "ascii_only": ascii_only,
            }

            # Add to in-memory messages list
            messages.append(sent_message)
            messages[:] = messages[-100:]  # Keep last 100

            # Save to log file
            log_path = Path("logs/sms.jsonl")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(sent_message, ensure_ascii=False) + "\n")

            return jsonify(
                {
                    "success": True,
                    "message": "SMS sent successfully!",
                    "ascii_only": ascii_only,
                    "preview": preview if not ascii_only else None,
                }
            )
        else:
            return jsonify({"success": False, "error": "Failed to send SMS"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/connect", methods=["POST"])
def connect_modem():
    """Connect to the modem."""
    global modem, modem_port, modem_connected, receiving_thread, stop_receiving

    try:
        # Use core sim7600 package to find modem
        port = find_sim7600_port()
        if not port:
            return jsonify({"success": False, "error": "Modem not found"}), 404

        # Open modem using core sim7600 package (with lock)
        with modem_lock:
            modem = Modem(port, echo_raw=True)  # Enable debug output
            modem.open()
            modem.init_sms_push()

        modem_port = port
        modem_connected = True

        # Start receiving thread
        stop_receiving = False
        receiving_thread = threading.Thread(target=receive_sms_loop, daemon=True)
        receiving_thread.start()

        return jsonify({"success": True, "port": port})

    except Exception as e:
        modem_connected = False
        return jsonify({"success": False, "error": str(e)}), 500


def run_dashboard(host="127.0.0.1", port=5000, debug=False):
    """Run the web dashboard."""
    try:
        print(f"\n🌐 SIM7600 Web Dashboard")
        print(f"{'='*50}")
        print(f"   URL: http://{host}:{port}")
        print(f"   Press Ctrl+C to stop")
        print(f"{'='*50}\n")
    except UnicodeEncodeError:
        # Fallback for Windows console that doesn't support emojis
        print(f"\nSIM7600 Web Dashboard")
        print(f"{'='*50}")
        print(f"   URL: http://{host}:{port}")
        print(f"   Press Ctrl+C to stop")
        print(f"{'='*50}\n")

    # Load existing messages
    load_existing_messages()
    try:
        print(f"✅ Loaded {len(messages)} existing messages")
    except UnicodeEncodeError:
        print(f"[OK] Loaded {len(messages)} existing messages")

    # Try to auto-connect to modem
    try:
        global modem, modem_port, modem_connected, receiving_thread, stop_receiving
        port_found = find_sim7600_port()
        if port_found:
            # Use lock for modem initialization
            with modem_lock:
                modem = Modem(port_found, echo_raw=True)  # Enable debug output
                modem.open()
                modem.init_sms_push()
            modem_port = port_found
            modem_connected = True
            try:
                print(f"✅ Connected to modem on {port_found}")
            except UnicodeEncodeError:
                print(f"[OK] Connected to modem on {port_found}")

            # Start receiving thread
            stop_receiving = False
            receiving_thread = threading.Thread(target=receive_sms_loop, daemon=True)
            receiving_thread.start()
            try:
                print(f"✅ Started SMS receiver")
            except UnicodeEncodeError:
                print(f"[OK] Started SMS receiver")
        else:
            try:
                print(
                    "⚠️  Modem not found. You can connect manually from the dashboard."
                )
            except UnicodeEncodeError:
                print(
                    "[WARNING] Modem not found. You can connect manually from the dashboard."
                )
    except Exception as e:
        try:
            print(f"⚠️  Could not auto-connect to modem: {e}")
        except UnicodeEncodeError:
            print(f"[WARNING] Could not auto-connect to modem: {e}")

    try:
        print(f"\n🚀 Opening dashboard at http://{host}:{port}")
        print(f"   (The browser should open automatically)\n")
    except UnicodeEncodeError:
        print(f"\n[STARTING] Opening dashboard at http://{host}:{port}")
        print(f"   (The browser should open automatically)\n")

    app.run(host=host, port=port, debug=debug, use_reloader=False)
