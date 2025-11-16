# Creative Content Security Lab

[![Focus: Content Security](https://img.shields.io/badge/Focus-Content%20Security-blue)]()
[![Domain: Creative Pipelines](https://img.shields.io/badge/Domain-Creative%20Pipelines-green)]()
[![Built With: Python](https://img.shields.io/badge/Built%20With-Python%20%2B%20Docker-lightgrey)]()
[![Use Case: Research Lab](https://img.shields.io/badge/Use%20Case-Research%20Lab-orange)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)]()

A practical home lab that explores how studios can protect high-value creative content  
such as interactive builds, cinematic files, pre-release media, 3D assets, and marketing materials  
across distributed workflows and global vendor ecosystems.

## About this project

This is a hands-on research lab for **creative content security**.  

It simulates how a studio might protect high-value digital assets—characters, environments, cinematics, interactive builds, and marketing materials—as they move through:

- internal creative teams  
- build and packaging pipelines  
- external vendors and partners  
- distributed delivery environments  

The code is intentionally small and runnable on a single machine.  
The goal is to show **end-to-end patterns** that apply across gaming, film, TV, advertising, VFX, in-flight entertainment, and streaming content workflows—not to recreate any one company’s environment.

## Table of contents

1. [Motivation](#motivation)  
2. [What this lab is](#what-this-lab-is)  
3. [High level architecture](#high-level-architecture)  
4. [Scenarios this lab covers](#scenarios-this-lab-covers)  
5. [Lab components](#lab-components)  
6. [Getting started](#getting-started)  
7. [Walking through a full scenario](#walking-through-a-full-scenario)  
8. [Folder structure](#folder-structure)  
9. [How this maps to real studios](#how-this-maps-to-real-studios)  
10. [Roadmap](#roadmap)  
11. [Real-world inspiration](#real-world-inspiration)  
12. [License](#license)

## Motivation

Living in Los Angeles and working at Media Arts Lab exposed me to some of the most complex creative ecosystems in the world—VFX houses, animation studios, trailer vendors, editorial teams, color and finishing facilities, audio post, and global marketing partners.  
Each one touches high-value, pre-release content before it ever reaches the public.

Later, as **Head of Security at Panasonic Avionics**, I worked directly with Hollywood studios to securely ingest, encrypt, distribute, and protect pre-release **TV, movie, and gaming content** for in-flight entertainment systems across hundreds of airlines.  
This included:

- multi-vendor content ingestion  
- transcoding workflows  
- region-specific distribution  
- DRM enforcement  
- pre-release embargo protection  
- leak prevention  
- secure storage and on-device playback  
- end-to-end audit and traceability  

Across both experiences, one thing became clear:

**Creative pipelines are some of the most distributed, high-risk, and dynamic environments in security.**

Many teams.  
Many vendors.  
Many tools.  
Many distribution paths.  
One shared challenge: **protecting high-value digital IP.**

This lab is a personal research project exploring those challenges.  
It is not tied to any one company or industry—its patterns apply to:

- game studios  
- VFX and animation pipelines  
- advertising and creative agencies  
- studios distributing theatrical or streaming content  
- AR/VR interactive experiences  
- global post-production ecosystems  

The goal is to build an approachable, end-to-end environment that demonstrates how creative content can be secured across its full lifecycle.

## What this lab is

This repository is a small reference environment that simulates a creative studio working with sensitive, high-value assets.

You will see:

- a fake creative project with 3D and image assets  
- a simple build pipeline that produces “interactive content builds”  
- a mock vendor portal for external partners  
- an activity logging and detection layer  
- basic watermarking and leak tracing  
- insider threat and vendor misuse simulations  

The purpose is not to build a production-grade system—it is to explore the patterns, workflows, and security controls that real studios use to protect content.

## High level architecture

There are five major zones:

1. **Studio Project Repo** – assets, manifests, registry  
2. **Build & Packaging Pipeline** – SBOM, signing, encryption  
3. **Vendor Access Portal** – controlled distribution, watermarking  
4. **Monitoring Layer** – logs, detection logic, anomaly checks  
5. **Leak & Insider Threat Simulations** – realistic failure scenarios  

A complete lifecycle is demonstrated:  
**from asset creation → build → vendor distribution → monitoring → incident analysis.**

### Diagram

```mermaid
flowchart LR
    A[Creators & Studio Repo\n(project/)] --> B[Build & Packaging Pipeline\n(pipeline/)]
    B --> C[Signed & Encrypted Builds\n(builds/)]
    C --> D[Vendor Portal\n(vendor_portal/)]
    D -->|Downloads & Watermarked Packages| E[Vendor Systems\n(simulated)]
    C --> F[Monitoring & Events\n(monitoring/)]
    D --> F
    E --> G[Leak & Insider Simulations\n(simulations/)]
    G --> F
    F --> H[Alerts & Analysis\n(monitoring/alerts)]
```

## Scenarios this lab covers

### 1. Pre-release asset control

- tracking asset lineage  
- identifying who touched what  
- tracing leaks using unique watermarks  

### 2. Vendor & partner risk

- time-limited access  
- controlled distribution  
- audit trails  
- watermark-based attribution  

### 3. Insider threat in creative pipelines

- unusual file activity  
- honeytokens  
- off-hours access detection  

### 4. Asset movement from dev → marketing → external partners

- ensuring provenance stays intact  
- maintaining auditability across multiple handoffs  

These scenarios mirror real-world content protection challenges in media, gaming, and entertainment.

## Lab components

### 1. Studio project repository

Path: `./project`

This represents a creative project with sensitive assets.

Contents:

- `assets/characters` – character images and models  
- `assets/environments` – backgrounds or environment art  
- `assets/cinematics` – stills or short clips that stand in for cinematic shots  
- `config/build_manifest.yml` – a definition of what goes into a build  
- `metadata/asset_registry.json` – a registry that tracks ownership and sensitivity  

Key ideas:

- Every asset has an identifier and a sensitivity level.  
- Assets in the registry can be traced through the rest of the lab.  
- The project can be treated like a game project, an animation, or an interactive experience.

### 2. Build and packaging pipeline

Path: `./pipeline`

This is a small build system written in Python.

Main entry points:

- `build.py` – reads the manifest and assembles a build directory  
- `generate_sbom.py` – creates a basic bill of materials in JSON  
- `sign.py` – creates a simple signature file for the build  
- `encrypt.py` – encrypts the build for a specific recipient  

Process summary:

1. Read the manifest.  
2. Collect the listed assets into a build directory.  
3. Generate an SBOM with references back to the asset registry.  
4. Sign the SBOM and the build manifest.  
5. Encrypt the final package for a target vendor or internal user.

This pipeline shows how even simple builds can carry provenance and traceable metadata.

### 3. Vendor access portal

Path: `./vendor_portal`

A small web application built with FastAPI.

Main features:

- sign in with a vendor id and shared secret  
- a view that lists builds available to that vendor  
- download links that embed a unique watermark, log the download event with time and vendor id, and set a time-based expiry  

Example flows:

- Vendor A logs in and downloads “Interactive Preview Build 01”.  
- The build created for Vendor A has a unique watermark id.  
- If a leak appears later you can match the watermark back to Vendor A.

### 4. Monitoring and detection layer

Path: `./monitoring`

This is where all the events come together.

Sources:

- build logs from `./pipeline/logs`  
- vendor download logs from `./vendor_portal/logs`  
- file access logs from local simulations in `./simulations`  

Core parts:

- `event_collector.py` – reads logs and normalizes them  
- `rules_engine.py` – simple rule checks such as downloads from unknown vendors, access to high sensitivity assets during unusual hours, builds created for vendors that no longer have active agreements  
- `anomaly_checks.py` – optional heuristics  

Output:

- alerts printed to the console  
- optional JSON alerts in `./monitoring/alerts`  

### 5. Leak and insider simulations

Path: `./simulations`

Scripts:

- `simulate_insider_copy.py` – copies assets into a personal directory and emits events  
- `simulate_vendor_leak.py` – takes a vendor-specific package and outputs a leaked copy with watermark preserved  
- `simulate_normal_usage.py` – simulates ordinary vendor and internal use for baseline  

When you run these simulations the monitoring layer will react and produce alerts.

## Getting started

### 1. Prerequisites

You will need:

- Git  
- Python 3.11 or later  

Optional but recommended:

- Docker and Docker Compose  
- A virtual environment tool such as `venv` or `pipenv`  

### 2. Clone the repository

```bash
git clone https://github.com/your-username/creative-content-security-lab.git
cd creative-content-security-lab
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Initialize sample data

Run the provided script to create example assets, manifests, and registry entries.

```bash
python scripts/bootstrap_lab.py
```

### 6. Run the build pipeline

```bash
python pipeline/build.py
python pipeline/generate_sbom.py
python pipeline/sign.py
python pipeline/encrypt.py
```

### 7. Start the vendor portal

```bash
uvicorn vendor_portal.app:app --reload
```

### 8. Start the monitoring layer

```bash
python monitoring/event_collector.py
python monitoring/rules_engine.py
```

## Walking through a full scenario

### Scenario: Vendor specific leak trace

Goal: Show how a vendor-specific build can be traced if a copy appears outside the portal.

Steps:

1. **Create a build for Vendor A**

   ```bash
   python pipeline/build.py
   python pipeline/generate_sbom.py
   python pipeline/sign.py
   python pipeline/encrypt.py
   ```

2. **Vendor A downloads the build**

   - Start the vendor portal if it is not running.  
   - Sign in as `vendor_a`.  
   - Download the available build.

3. **Simulate a leak**

   In a new terminal:

   ```bash
   python simulations/simulate_vendor_leak.py --vendor vendor_a --build-id build_001
   ```

4. **Run detection**

   ```bash
   python monitoring/event_collector.py
   python monitoring/rules_engine.py
   ```

   The rules engine will compare the watermark from the leaked file against the watermark assignments and raise an alert that the leak matches a build created for Vendor A.

## Folder structure

```
creative-content-security-lab/
  README.md
  requirements.txt
  scripts/
    bootstrap_lab.py
  project/
    assets/
      characters/
      environments/
      cinematics/
    config/
      build_manifest.yml
    metadata/
      asset_registry.json
  pipeline/
    build.py
    generate_sbom.py
    sign.py
    encrypt.py
    logs/
  vendor_portal/
    app.py
    data/
    logs/
  monitoring/
    event_collector.py
    rules_engine.py
    anomaly_checks.py
    alerts/
  simulations/
    simulate_insider_copy.py
    simulate_vendor_leak.py
    simulate_normal_usage.py
    leaks/
    logs/
  docs/
    architecture-diagram.png
```

## How this maps to real studios

This lab reflects patterns seen in **gaming**, **film**, **television**, **animation**, **VFX**, **advertising**, and **in-flight entertainment** environments:

- The `project` directory simulates a creative build tree (game project, VFX sequence, marketing campaign, or pre-release film assets).  
- The build pipeline represents dailies creation, interactive demo builds, trailer cuts, or internal previews.  
- The vendor portal represents external collaborators—localization, trailer houses, marketing agencies, post-production vendors, regional distributors, or authorized integrators.  
- The monitoring layer simulates the SIEM and content access logs that real studios monitor.  
- Leak simulations mirror real tensions: internal misuse, vendor leaks, accidental oversharing, or unauthorized redistribution.  

This lab is intentionally small so it can run on a single machine, but the patterns scale to global studio ecosystems like:

- game publishers  
- theatrical distribution  
- streaming content workflows  
- large advertising agencies  
- in-flight entertainment pipelines  
- post-production ecosystems  

## Roadmap

Planned improvements and stretch ideas.

**Short term:**

- Add a simple web dashboard for alerts.  
- Add role-based access control to the vendor portal.  
- Add more realistic asset types and metadata.  
- Add a basic policy file that describes which assets can leave the studio.  

**Medium term:**

- Add optional support for OpenSearch or Elastic for events.  
- Add a simple anomaly detector that looks at access patterns over time.  
- Integrate a basic command-line helper to run end-to-end scenarios.  

**Long term:**

- Experiment with stronger watermarking techniques.  
- Explore integration with signing and attestation tools.  
- Add a separate “anti-cheat telemetry” mini module for interactive builds.  

Suggestions and pull requests are welcome.

## Real-world inspiration

This lab is inspired by real challenges seen in:

- Los Angeles–based creative ecosystems (Media Arts Lab, global agencies, production and post-production workflows).  
- Studio content distribution for in-flight entertainment (Panasonic Avionics).  
- The broader problem of moving pre-release IP through complex, distributed vendor networks.  

Common threads in those environments include:

- **High-value IP** that must not leak before release.  
- **Many vendors and partners** touching the same assets.  
- **Multi-stage pipelines** (ingest → edit → localize → finish → distribute).  
- **Global scale** and varied infrastructure.  
- **Tight timeframes** with creative teams under pressure.  

This project distills those patterns into a small, reproducible environment that security teams, engineers, and technical leaders can use to explore content protection ideas without needing access to proprietary systems.

## License

MIT License – see `LICENSE`.
