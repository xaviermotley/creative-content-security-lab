#!/usr/bin/env python3
import json
from pathlib import Path
from rich import print

ROOT = Path(__file__).resolve().parents[1]
BUILDS_DIR = ROOT / "builds"

def main(build_id: str | None = None):
    if build_id is None:
        # naive: pick the latest directory name
        build_ids = sorted([p.name for p in BUILDS_DIR.iterdir() if p.is_dir()])
        if not build_ids:
            raise SystemExit("No builds found")
        build_id = build_ids[-1]

    build_root = BUILDS_DIR / build_id
    meta_path = build_root / "build_meta.json"
    if not meta_path.exists():
        raise SystemExit(f"No build_meta.json found for build {build_id}")

    build_meta = json.loads(meta_path.read_text(encoding="utf-8"))

    sbom = {
        "build_id": build_meta["build_id"],
        "created_at": build_meta["created_at"],
        "components": [],
    }

    for asset in build_meta["assets"]:
        sbom["components"].append(
            {
                "id": asset["id"],
                "path": asset["path"],
                "owner": asset["owner"],
                "sensitivity": asset["sensitivity"],
                "type": "creative-asset",
            }
        )

    sbom_path = build_root / "sbom.json"
    sbom_path.write_text(json.dumps(sbom, indent=2), encoding="utf-8")

    print(f"[green]SBOM written to {sbom_path}[/green]")


if __name__ == "__main__":
    main()
