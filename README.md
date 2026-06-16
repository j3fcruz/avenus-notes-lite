<div align="center">

<img src="assets/icons/sticky_icon.ico" alt="Avernus Notes Logo" width="96" height="96"/>

# Avernus Notes — Lite Edition

**v1.0.0** · Built by [PatronHubDevs Technologies](https://github.com/j3fcruz) · 🇵🇭 Philippines

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#-license)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?logo=qt)](https://doc.qt.io/qtforpython/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows)](https://github.com/j3fcruz)
[![Offline](https://img.shields.io/badge/Offline-First-success)](#-privacy)

> **Simple. Fast. Lightweight. Just notes.**  
> A lightweight, always-available desktop sticky notes app — inspired by Windows Sticky Notes, built for zero-friction productivity.

[Download](#-installation) · [Screenshots](#-screenshots) · [Build from Source](#-build) · [Upgrade to Pro](#-upgrade-to-pro)

---

</div>

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Build](#-build)
- [Limitations (Lite Edition)](#-limitations-lite-edition)
- [Upgrade to Pro](#-upgrade-to-pro)
- [Privacy](#-privacy)
- [License](#-license)
- [Author](#-author)

---

## Overview

**Avernus Notes — Lite Edition** is a minimalist, offline-first desktop sticky notes application built with **Python** and **PySide6**. It is designed for users who want the classic "Post-it" experience on their desktop without the overhead of accounts, cloud syncing, or complex encryption.

Refactored from the Avernus Secure suite, this edition focuses on speed and ease of use while maintaining a clean, modular codebase.

---

## Features

### ⚡ Instant & Lightweight
- **Zero Login**: Opens directly to your notes instantly.
- **Low Footprint**: Optimized for minimal CPU and RAM usage.

### 🎨 Flexible UI
- **Multiple Notes**: Create unlimited floating note windows.
- **Customizable**: 7 distinct color themes — click the toolbar dot to cycle.
- **Always-on-Top**: Pin important notes to stay visible above other windows.

### 🛠️ Productivity
- **Autosave**: Saves automatically (800ms debounce) after every edit.
- **System Tray**: Minimize all notes to the tray and restore them with a single click.
- **Resize & Move**: Drag to move or resize notes exactly where you need them.

### 📂 Open Data
- **Plaintext Storage**: Notes are saved as human-readable JSON. No proprietary lock-in.

---

## Screenshots

| Main Sticky Note | System Tray Menu |
|--------|----------------|
| ![Main UI](assets/icons/sticky_icon.png) | *Screenshot Coming Soon* |

---

## Project Structure

```
Avernus_Notes/
├── main.py               # Entry point
├── requirements.txt      # Dependencies
├── config/
│   └── settings.py       # Tunable constants (colors, delays, etc.)
├── core/
│   ├── note_manager.py   # Note lifecycle management
│   └── storage.py        # Atomic JSON read/write logic
├── ui/
│   ├── sticky_note.py    # Main Note Window (Qt Widgets)
│   ├── tray.py           # System tray integration
│   └── styles.py         # QSS Stylesheets
├── utils/                # Helper utilities
└── assets/               # Icons and graphical resources
```

---

## Installation

### Option 1 — Prebuilt Binary (Recommended)

1. Download the latest release from the [Releases](https://github.com/j3fcruz/avenus-notes-lite/releases) section.
2. Extract the ZIP archive.
3. Run `AvernusNotesLite.exe`.

### Option 2 — Run from Source

**Requirements:** Python 3.10+, Windows

```bash
# Clone the repository
git clone https://github.com/j3fcruz/avenus-notes-lite.git
cd avenus-notes-lite

# Install dependencies
pip install -r requirements.txt

# Launch
python main.py
```

---

## Build

### Nuitka (Recommended for Production)

```bash
pip install nuitka zstandard ordered-set

nuitka --onefile --windows-disable-console \
       --windows-icon-from-ico=assets/icons/sticky_icon.ico \
       --include-data-dir=assets=assets \
       --output-filename=AvernusNotesLite.exe \
       main.py
```

---

## Limitations (Lite Edition)

The Lite Edition is built for simplicity. For advanced security and power-user features, consider the Pro Edition.

| Feature | Lite | Pro |
|--------|------|-----|
| Multiple Notes | ✅ | ✅ |
| Autosave | ✅ | ✅ |
| Custom Colors | ✅ | ✅ |
| Encryption | ❌ (Plaintext) | ✅ (AES-256) |
| Master Password | ❌ | ✅ |
| Hardware Binding | ❌ | ✅ |
| Secure Backups | ❌ | ✅ |

---

## Upgrade to Pro

**Avernus Notes Pro** adds a powerful security layer to your desktop notes:

- **Military-Grade Encryption**: Every note is encrypted with AES-256.
- **Master Password Protection**: Lock your entire note collection.
- **Rust-Powered Core**: High-performance cryptographic operations.
- **Secure File Shredding**: Ensures deleted notes are unrecoverable.

> [**Upgrade on Gumroad →**](https://patronhubdevs.gumroad.com/l/lgaqim)

---

## Privacy

Avernus Notes Lite is 100% private:

- **No telemetry**: We don't track what you write or how you use the app.
- **Offline only**: No network requests are ever made.
- **Local storage**: Your data never leaves your machine.

---

## License

**MIT License** — Free for personal and commercial use. See `LICENSE` for details.

---

## Author

**Marco Polo**  
PatronHubDevs Technologies  
🇵🇭 Philippines  
[GitHub](https://github.com/j3fcruz) · [Gumroad](https://patronhubdevs.gumroad.com/l/lgaqim)

---

<div align="center">

**Avernus Notes** · PatronHubDevs Technologies · Philippines  
*Fast. Clean. Private. No compromises.*

</div>
