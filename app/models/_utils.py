from datetime import datetime, timezone


def utcnow() -> datetime:
    """UTC sem timezone (mesmo formato já gravado no banco)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)
