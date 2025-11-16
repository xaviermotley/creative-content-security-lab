#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
from rich import print

ROOT = Path(__file__).resolve().parents[1]
MON_DIR = ROOT / "monitoring"
ALERTS_DIR = MON_DIR / "alerts"
EVENTS_PATH = MON_DIR / "events.json"

ALERTS_DIR.mkdir(parents=True, exist_ok=True)

def load_events():
    if not EVENTS_PATH.exists():
        return []
    return json.loads(EVENTS_PATH.read_text(encoding="utf-8"))

def rule_download_after_expiry(event):
    if event["type"] != "vendor_download":
        return None
    expires_at = datetime.fromisoformat(event["expires_at"].replace("Z", "+00:00"))
    downloaded_at = datetime.fromisoformat(event["downloaded_at"].replace("Z", "+00:00"))
    if downloaded_at > expires_at:
        return {
            "rule": "download_after_expiry",
            "severity": "medium",
            "message": f"Vendor {event['vendor_id']} downloaded build {event['build_id']} after expiry.",
            "event": event,
        }
    return None

def rule_high_sensitivity_vendor(event):
    # placeholder example: flag high sensitivity builds going to vendors not in an allowlist
    if event["type"] != "build_created":
        return None
    # Additional rules could inspect build metadata
    return None

def main():
    events = load_events()
    alerts = []
    for ev in events:
        for rule in (rule_download_after_expiry, rule_high_sensitivity_vendor):
            alert = rule(ev)
            if alert:
                alerts.append(alert)
                print(f"[red]ALERT:[/red] {alert['message']}")
    alerts_path = ALERTS_DIR / "alerts.json"
    alerts_path.write_text(json.dumps(alerts, indent=2), encoding="utf-8")
    print(f"[green]{len(alerts)} alerts written to {alerts_path}[/green]")

if __name__ == "__main__":
    main()
