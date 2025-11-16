#!/usr/bin/env python3
import json
import shutil
from datetime import datetime
from pathlib import Path

import yaml
from rich import print

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "project"
PIPELINE_LOGS = ROOT / "pipeline" / "logs"
BUILDS_DIR = ROOT / "builds"

PIPELINE_LOGS.mkdir(parents=True, exist_ok=True)
BUILDS_DIR.mkdir(parents=True, exist_ok=True)


def load_asset_registry():
    registry_path = PROJECT_DIR / "metadata" / "asset_registry.json"
    return {a["id"]: a for a in json.loads(registry_path.read_text(encoding="utf-8"))}


def load_manifest():
    manifest_path = PROJECT_DIR / "config" / "build_manifest.yml"
    return yaml.safe_load(manifest_path.read_text(encoding="utf-8"))


def copy_asset(asset_info, build_root: Path):
    src_path = PROJECT_DIR / asset_info["path"]
    dest_path = build_root / asset_info["path"]
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_path)


def main():
    manifest = load_manifest()
    registry = load_asset_registry()

    build_id = manifest["build_id"]
    build_root = BUILDS_DIR / build_id
    build_root.mkdir(parents=True, exist_ok=True)

    print(f"[bold cyan]Building {build_id}[/bold cyan]")

    used_assets = []
    for a in manifest.get("assets", []):
        asset_id = a["id"]
        asset_info = registry.get(asset_id)
        if not asset_info:
            print(f"[yellow]Warning: asset id {asset_id} not found in registry[/yellow]")
            continue
        copy_asset(asset_info, build_root)
        used_assets.append(asset_info)

    build_meta = {
        "build_id": build_id,
        "description": manifest.get("description", ""),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "assets": used_assets,
        "target_vendors": manifest.get("target_vendors", []),
    }

    meta_path = build_root / "build_meta.json"
    meta_path.write_text(json.dumps(build_meta, indent=2), encoding="utf-8")

    # log event
    build_events_path = PIPELINE_LOGS / "build_events.json"
    if build_events_path.exists():
        events = json.loads(build_events_path.read_text(encoding="utf-8"))
    else:
        events = []

    events.append(
        {
            "type": "build_created",
            "build_id": build_id,
            "timestamp": build_meta["created_at"],
            "target_vendors": build_meta["target_vendors"],
        }
    )
    build_events_path.write_text(json.dumps(events, indent=2), encoding="utf-8")

    print(f"[green]Build {build_id} created at {build_root}[/green]")


if __name__ == "__main__":
    main()
