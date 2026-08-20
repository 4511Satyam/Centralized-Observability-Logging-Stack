import json
import logging
import sys
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "text-summarization",
            "message": record.getMessage(),
        }
        if hasattr(record, "event"):
            payload["event"] = record.event
        if hasattr(record, "latency_ms"):
            payload["latency_ms"] = record.latency_ms
        if hasattr(record, "input_tokens"):
            payload["input_tokens"] = record.input_tokens
        if hasattr(record, "output_tokens"):
            payload["output_tokens"] = record.output_tokens
        return json.dumps(payload)

def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)
