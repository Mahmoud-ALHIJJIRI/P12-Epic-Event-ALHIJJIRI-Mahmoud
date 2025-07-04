"""
🛡️ Sentry Integration for Epic Events CRM

This module initializes the Sentry SDK for error tracking and performance monitoring.
It loads configuration from environment variables and attaches user and error context.
"""

# 📦 External Imports ───────────────────────────────────────────────
import os
import sentry_sdk
from dotenv import load_dotenv


# 🚀 Initialize Sentry SDK ──────────────────────────────────────────
def init_sentry():
    """
    Load the SENTRY_DSN from environment and initialize the Sentry SDK with tracking enabled.
    """
    load_dotenv()
    dsn = os.getenv("SENTRY_DSN")

    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            send_default_pii=True,
            environment="production",  # or "development"
            traces_sample_rate=1.0
        )
