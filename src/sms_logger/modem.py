from __future__ import annotations
import time
import serial
from serial.tools import list_ports
from typing import Iterable


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

    def _drain(self, dur: float = 0.5):
        t0 = time.time()
        while time.time() - t0 < dur:
            _ = self.readline()

    def lines(self) -> Iterable[str]:
        while True:
            yield self.readline()
