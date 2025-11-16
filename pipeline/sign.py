#!/usr/bin/env python3
import hashlib
from pathlib import Path
from rich import print
import json

ROOT = Path(__file__).resolve().parents[1]
BUILDS_DIR = ROOT / "builds"

def main(build_id: str | None = None):
    if build_id is None:
        build_ids = sorted([p.name for p in BUILDS_DIR.iterdir() if p.is_dir()])
        if not build_ids:
            raise SystemExit("No builds found")
        build_id = build_ids[-1]

    build_root = BUILDS_DIR / build_id
    meta_path = build_root / "build_meta.json"
    sbom_path = build_root / "sbom.json"

    if not meta_path.exists() or not sbom_path.exists():
        raise SystemExit("Missing build_meta.json or sbom.json")

    h = hashlib.sha256()
    h.update(meta_path.read_bytes())
    h.update(sbom_path.read_bytes())
    digest = h.hexdigest()

    sig = {
        "build_id": build_id,
        "alg": "SHA256",
        "digest": digest,
    }

    sig_path = build_root / "signature.json"
    sig_path.write_text(json.dumps(sig, indent=2), encoding="utf-8")

    print(f"[green]Signature written to {sig_path}[/green]")

if __name__ == "__main__":
    main()
