#!/usr/bin/env python3
"""
Placeholder for anomaly detection logic.

In the future this module could:
- build simple baselines of vendor download frequency
- flag unusual activity windows (e.g., odd hours)
- look for spikes in build creation or downloads
"""
from pathlib import Path
import json
from rich import print

ROOT = Path(__file__).resolve().parents[1]
MON_DIR = ROOT / "monitoring"
EVENTS_PATH = MON_DIR / "events.json"

def main():
    if not EVENTS_PATH.exists():
        print("[yellow]No events.json found; run event_collector first.[/yellow]")
        return
    events = json.loads(EVENTS_PATH.read_text(encoding="utf-8"))
    print(f"[cyan]Loaded {len(events)} events for future anomaly analysis.[/cyan]")

if __name__ == "__main__":
    main()
