#!/usr/bin/env python3
import json
from pathlib import Path
from cryptography.fernet import Fernet
from rich import print

ROOT = Path(__file__).resolve().parents[1]
BUILDS_DIR = ROOT / "builds"
KEYS_DIR = ROOT / "secrets"

KEYS_DIR.mkdir(parents=True, exist_ok=True)

def get_vendor_key(vendor_id: str) -> bytes:
    key_path = KEYS_DIR / f"{vendor_id}.key"
    if key_path.exists():
        return key_path.read_bytes()
    key = Fernet.generate_key()
    key_path.write_bytes(key)
    print(f"[yellow]Generated new key for {vendor_id} at {key_path}[/yellow]")
    return key

def main(build_id: str | None = None):
    if build_id is None:
        build_ids = sorted([p.name for p in BUILDS_DIR.iterdir() if p.is_dir()])
        if not build_ids:
            raise SystemExit("No builds found")
        build_id = build_ids[-1]

    build_root = BUILDS_DIR / build_id
    meta_path = build_root / "build_meta.json"
    if not meta_path.exists():
        raise SystemExit("Missing build_meta.json")

    build_meta = json.loads(meta_path.read_text(encoding="utf-8"))
    target_vendors = build_meta.get("target_vendors", [])
    if not target_vendors:
        print("[yellow]No target vendors defined; nothing to encrypt[/yellow]")
        return

    # package: zip whole build directory (excluding any existing archives)
    archive_path = build_root / f"{build_id}.zip"
    if not archive_path.exists():
        from shutil import make_archive
        make_archive(str(archive_path.with_suffix("")), "zip", root_dir=build_root)

    for vendor_id in target_vendors:
        key = get_vendor_key(vendor_id)
        f = Fernet(key)
        data = archive_path.read_bytes()
        token = f.encrypt(data)
        out_path = build_root / f"{build_id}_{vendor_id}.enc"
        out_path.write_bytes(token)
        print(f"[green]Encrypted package for {vendor_id} at {out_path}[/green]")

if __name__ == "__main__":
    main()
