"""
Web dashboard for SIM7600 SMS Manager.
A separate package that uses the core sim7600 package.
"""

from .app import run_dashboard

__version__ = "0.1.0"
__all__ = ["run_dashboard"]


