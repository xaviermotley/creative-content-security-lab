#!/usr/bin/env python3
import json
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_yaml(path: Path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def bootstrap_project():
    project_dir = ROOT / "project"
    assets_dir = project_dir / "assets"
    chars_dir = assets_dir / "characters"
    env_dir = assets_dir / "environments"
    cin_dir = assets_dir / "cinematics"
    config_dir = project_dir / "config"
    meta_dir = project_dir / "metadata"

    for d in (chars_dir, env_dir, cin_dir, config_dir, meta_dir):
        ensure_dir(d)

    # Simple placeholder "assets"
    (chars_dir / "hero.txt").write_text("HERO CHARACTER ASSET", encoding="utf-8")
    (env_dir / "cityscape.txt").write_text("CITYSCAPE ENVIRONMENT ASSET", encoding="utf-8")
    (cin_dir / "intro_scene.txt").write_text("INTRO CINEMATIC ASSET", encoding="utf-8")

    asset_registry = [
        {
            "id": "char_hero",
            "path": "assets/characters/hero.txt",
            "owner": "studio_internal",
            "sensitivity": "high",
        },
        {
            "id": "env_cityscape",
            "path": "assets/environments/cityscape.txt",
            "owner": "studio_internal",
            "sensitivity": "medium",
        },
        {
            "id": "cin_intro",
            "path": "assets/cinematics/intro_scene.txt",
            "owner": "studio_internal",
            "sensitivity": "high",
        },
    ]
    write_json(meta_dir / "asset_registry.json", asset_registry)

    build_manifest = {
        "build_id": "build_001",
        "description": "Interactive Preview Build 01",
        "assets": [
            {"id": "char_hero"},
            {"id": "env_cityscape"},
            {"id": "cin_intro"},
        ],
        "target_vendors": ["vendor_a"],
    }
    write_yaml(config_dir / "build_manifest.yml", build_manifest)


def bootstrap_vendors():
    vendor_dir = ROOT / "vendor_portal"
    data_dir = vendor_dir / "data"
    logs_dir = vendor_dir / "logs"
    for d in (data_dir, logs_dir):
        ensure_dir(d)

    vendors = [
        {"id": "vendor_a", "name": "Vendor A Localization", "secret": "vendor_a_secret"},
        {"id": "vendor_b", "name": "Vendor B Trailer House", "secret": "vendor_b_secret"},
    ]
    write_json(data_dir / "vendors.json", vendors)
    write_json(logs_dir / "downloads.json", [])


def bootstrap_monitoring():
    mon_dir = ROOT / "monitoring"
    alerts_dir = mon_dir / "alerts"
    ensure_dir(alerts_dir)
    # empty placeholder alert log
    (alerts_dir / "alerts.json").write_text("[]", encoding="utf-8")


def bootstrap_simulations():
    sim_dir = ROOT / "simulations"
    leaks_dir = sim_dir / "leaks"
    logs_dir = sim_dir / "logs"
    for d in (sim_dir, leaks_dir, logs_dir):
        ensure_dir(d)


def main():
    print("Bootstrapping Creative Content Security Lab...")
    bootstrap_project()
    bootstrap_vendors()
    bootstrap_monitoring()
    bootstrap_simulations()
    print("Done. You can now run the pipeline and portal.")


if __name__ == "__main__":
    main()
