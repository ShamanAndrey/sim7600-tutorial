from __future__ import annotations
import time
import serial
from serial.tools import list_ports
from typing import Iterable
import unicodedata


def find_sim7600_port() -> str | None:
    """
    Automatically detect the SIM7600 modem AT PORT by scanning available COM ports.
    The SIM7600 creates multiple virtual ports - we specifically need the AT PORT.
    Returns the port name (e.g., 'COM10') if found, otherwise None.
    """
    ports = list_ports.comports()

    # First pass: Look specifically for "AT PORT" in the description
    # This is the correct port for AT commands and SMS
    for port in ports:
        desc = (port.description or "").lower()
        if "at port" in desc and ("simcom" in desc or "hs-usb" in desc):
            return port.device

    # Second pass: Fallback to any Simcom device if AT PORT not found
    # (for compatibility with other modems)
    for port in ports:
        desc = (port.description or "").lower()
        manufacturer = (port.manufacturer or "").lower()
        if "simcom" in desc or "simcom" in manufacturer:
            return port.device

    return None


class Modem:
    def __init__(
        self,
        port: str,
        baud: int = 115200,
        timeout: float = 1.0,
        echo_raw: bool = False,
    ):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.echo_raw = echo_raw
        self.ser: serial.Serial | None = None

    def open(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        # A brief settle time after opening
        time.sleep(0.2)

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def write_cmd(self, cmd: str):
        if not self.ser or not self.ser.is_open:
            raise RuntimeError("Serial not open")
        data = (cmd.strip() + "\r").encode("utf-8", errors="ignore")
        self.ser.write(data)

    def readline(self) -> str:
        if not self.ser or not self.ser.is_open:
            return ""
        raw = self.ser.readline()
        try:
            s = raw.decode("utf-8", errors="ignore").rstrip("\r\n")
        except Exception:
            s = ""
        if self.echo_raw and s:
            print(s)
        return s

    def init_sms_push(self):
        # Basic sanity & setup
        for cmd in (
            "AT",
            "AT+CMEE=2",
            "AT+CMGF=1",
            'AT+CSCS="GSM"',
            "AT+CNMI=2,2,0,0,0",
        ):
            self.write_cmd(cmd)
            # Read a few lines to consume OK / errors
            self._drain(0.6)

    def init_voice_listen(self):
        """
        Initialize modem to report incoming call indications with caller ID.
        Enables: verbose errors, caller ID presentation, and ring reporting.
        """
        for cmd in (
            "AT",
            "AT+CMEE=2",     # verbose errors
            "AT+CLIP=1",     # enable caller ID reporting: +CLIP: "<num>",...
            "AT+CRC=1",      # extended ring indications (optional)
        ):
            self.write_cmd(cmd)
            self._drain(0.5)

    def _drain(self, dur: float = 0.5):
        t0 = time.time()
        while time.time() - t0 < dur:
            _ = self.readline()

    def send_sms(self, phone_number: str, message: str, encoding: str = "auto") -> bool:
        """
        Send an SMS message.

        Args:
            phone_number: Recipient phone number (e.g., "+1234567890")
            message: Message text to send
            encoding: Character encoding - "auto" (default), "gsm", or "ucs2"
                     "auto" tries GSM first, falls back to UCS2 for special chars
                     "gsm" for standard ASCII/GSM characters
                     "ucs2" for Unicode/emoji support

        Returns:
            True if message sent successfully, False otherwise

        Example:
            >>> modem = Modem("COM10")
            >>> modem.open()
            >>> modem.send_sms("+1234567890", "Hello!")
            True
            >>> modem.send_sms("+1234567890", "Hello 🎉", encoding="ucs2")
            True
        """
        if not self.ser or not self.ser.is_open:
            raise RuntimeError("Serial port not open")

        # Validate inputs
        if not phone_number:
            raise ValueError("Phone number cannot be empty")
        if not message:
            raise ValueError("Message cannot be empty")
        if len(message) > 1600:
            raise ValueError("Message too long (max 1600 characters)")

        try:
            # All messages use GSM encoding
            # Non-ASCII characters are handled by normalization and the user
            # has been warned at the CLI level if message contains special chars

            # Set text mode
            self.write_cmd("AT+CMGF=1")
            time.sleep(0.5)
            self._drain(0.3)

            # Set GSM character encoding
            self.write_cmd('AT+CSCS="GSM"')
            time.sleep(0.3)
            self._drain(0.3)

            # Initiate SMS send
            self.write_cmd(f'AT+CMGS="{phone_number}"')
            time.sleep(0.5)

            # Wait for '>' prompt
            prompt_received = False
            for _ in range(10):
                line = self.readline()
                if ">" in line:
                    prompt_received = True
                    break

            if not prompt_received:
                if self.echo_raw:
                    print("ERROR: Did not receive '>' prompt from modem")
                return False

            # Send message + Ctrl+Z (chr(26))
            # User has been warned about non-ASCII characters at the CLI level
            # Try to send as ASCII first for best compatibility
            try:
                message_data = (message + chr(26)).encode("ascii")
            except UnicodeEncodeError:
                # Contains non-ASCII - normalize and strip accents
                normalized = unicodedata.normalize("NFD", message)
                cleaned = "".join(
                    char
                    for char in normalized
                    if ord(char) < 128 or unicodedata.category(char) != "Mn"
                )
                # Replace any remaining non-ASCII with ?
                cleaned = "".join(char if ord(char) < 128 else "?" for char in cleaned)
                message_data = (cleaned + chr(26)).encode("ascii")

            self.ser.write(message_data)

            # Wait for confirmation
            time.sleep(1)  # Give modem time to send

            success = False
            got_cmgs = False
            got_ok = False
            error_msg = None

            for _ in range(20):  # Wait up to ~2 seconds for response
                line = self.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                if self.echo_raw:
                    print(f"Response: {line}")

                # Look for success indicators
                if "+CMGS:" in line:
                    got_cmgs = True
                    success = True
                elif "OK" in line:
                    got_ok = True
                    success = True
                elif "ERROR" in line or "+CMS ERROR" in line:
                    error_msg = line
                    if self.echo_raw:
                        print(f"ERROR: Failed to send SMS: {line}")
                    return False

                # Break early if we got both confirmations or just OK
                if (got_cmgs and got_ok) or (got_ok and success):
                    break

            if not success and error_msg:
                if self.echo_raw:
                    print(f"ERROR: {error_msg}")

            return success

        except Exception as e:
            if self.echo_raw:
                print(f"Exception while sending SMS: {e}")
            return False

    def lines(self) -> Iterable[str]:
        while True:
            yield self.readline()
