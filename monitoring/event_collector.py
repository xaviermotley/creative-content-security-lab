#!/usr/bin/env python3
import json
from pathlib import Path
from rich import print

ROOT = Path(__file__).resolve().parents[1]
PIPELINE_LOGS = ROOT / "pipeline" / "logs"
VENDOR_LOGS = ROOT / "vendor_portal" / "logs"
SIM_LOGS = ROOT / "simulations" / "logs"
MON_DIR = ROOT / "monitoring"
EVENTS_PATH = MON_DIR / "events.json"

MON_DIR.mkdir(parents=True, exist_ok=True)

def read_json_if_exists(path: Path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    events = []

    # Build events
    build_events = read_json_if_exists(PIPELINE_LOGS / "build_events.json")
    for e in build_events:
        e["source"] = "pipeline"
    events.extend(build_events)

    # Vendor downloads
    downloads = read_json_if_exists(VENDOR_LOGS / "downloads.json")
    for d in downloads:
        events.append({
            "type": "vendor_download",
            "source": "vendor_portal",
            **d,
        })

    # Simulated leak events (optional, placeholder)
    leak_events = []
    sim_events_path = SIM_LOGS / "events.json"
    if sim_events_path.exists():
        leak_events = json.loads(sim_events_path.read_text(encoding="utf-8"))
        for e in leak_events:
            e["source"] = "simulation"
    events.extend(leak_events)

    EVENTS_PATH.write_text(json.dumps(events, indent=2), encoding="utf-8")
    print(f"[green]Collected {len(events)} events into {EVENTS_PATH}[/green]")

if __name__ == "__main__":
    main()
