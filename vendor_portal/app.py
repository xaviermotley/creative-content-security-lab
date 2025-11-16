#!/usr/bin/env python3
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "vendor_portal" / "data"
LOGS_DIR = ROOT / "vendor_portal" / "logs"
BUILDS_DIR = ROOT / "builds"

app = FastAPI(title="Vendor Portal (Creative Content Security Lab)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_vendors():
    path = DATA_DIR / "vendors.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_downloads():
    path = LOGS_DIR / "downloads.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_downloads(downloads):
    path = LOGS_DIR / "downloads.json"
    path.write_text(json.dumps(downloads, indent=2), encoding="utf-8")


class VendorAuth(BaseModel):
    vendor_id: str
    secret: str


class BuildEntry(BaseModel):
    build_id: str
    description: str | None = None
    created_at: str
    watermark_id: str | None = None


def authenticate_vendor(auth: VendorAuth):
    vendors = load_vendors()
    for v in vendors:
        if v["id"] == auth.vendor_id and v["secret"] == auth.secret:
            return v
    raise HTTPException(status_code=401, detail="Invalid vendor credentials")


@app.post("/login")
def login(auth: VendorAuth):
    vendor = authenticate_vendor(auth)
    return {"status": "ok", "vendor": {"id": vendor["id"], "name": vendor["name"]}}


@app.post("/builds", response_model=List[BuildEntry])
def list_builds(auth: VendorAuth):
    vendor = authenticate_vendor(auth)
    vendor_id = vendor["id"]

    entries: List[BuildEntry] = []
    for build_dir in BUILDS_DIR.iterdir():
        if not build_dir.is_dir():
            continue
        meta_path = build_dir / "build_meta.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if vendor_id not in meta.get("target_vendors", []):
            continue
        entries.append(
            BuildEntry(
                build_id=meta["build_id"],
                description=meta.get("description"),
                created_at=meta["created_at"],
            )
        )

    return entries


@app.post("/download/{build_id}")
def download_build(build_id: str, auth: VendorAuth):
    vendor = authenticate_vendor(auth)
    vendor_id = vendor["id"]

    build_root = BUILDS_DIR / build_id
    enc_path = build_root / f"{build_id}_{vendor_id}.enc"
    if not enc_path.exists():
        raise HTTPException(status_code=404, detail="No encrypted package for this vendor/build")

    watermark_id = f"{build_id}:{vendor_id}"
    now = datetime.utcnow().isoformat() + "Z"

    downloads = load_downloads()
    downloads.append(
        {
            "vendor_id": vendor_id,
            "build_id": build_id,
            "watermark_id": watermark_id,
            "downloaded_at": now,
            "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z",
        }
    )
    save_downloads(downloads)

    # Instead of streaming file, just acknowledge and point to path in this MVP
    return {
        "status": "ok",
        "message": "Download recorded (in a real system this would return the encrypted file).",
        "watermark_id": watermark_id,
        "package_path": str(enc_path),
    }
