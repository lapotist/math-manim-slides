#!/usr/bin/env python3
"""Prepare the pinned, network-free TeX toolchain used by Manim."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "tex"
DVISVGM_RPMS = ROOT / "build" / "dvisvgm-rpm"
DVISVGM_ROOT = ROOT / "build" / "dvisvgm-root"
READY = OUTPUT / ".ready"


def command_succeeds(command: list[str]) -> bool:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def ensure_dvisvgm() -> None:
    """Provide dvisvgm without requiring privileged package installation."""
    if command_succeeds(["dvisvgm", "--version"]):
        return

    os_release = platform.freedesktop_os_release()
    if os_release.get("ID") != "fedora":
        raise SystemExit(
            "dvisvgm is required. Install it with your operating-system package "
            "manager, then rerun: pixi run prepare-tex"
        )
    if shutil.which("dnf") is None or shutil.which("bsdtar") is None:
        raise SystemExit(
            "Fedora setup needs the dnf download plugin and bsdtar. Install "
            "dnf-plugins-core and bsdtar, then rerun: pixi run prepare-tex"
        )

    DVISVGM_RPMS.mkdir(parents=True, exist_ok=True)
    DVISVGM_ROOT.mkdir(parents=True, exist_ok=True)
    print("dvisvgm is absent; downloading the Fedora package into build/ ...")
    subprocess.run(
        [
            "dnf",
            "download",
            "--resolve",
            "--destdir",
            str(DVISVGM_RPMS),
            "texlive-dvisvgm",
            "texlive-amsfonts",
        ],
        cwd=ROOT,
        check=True,
    )

    packages = sorted(DVISVGM_RPMS.glob("*.rpm"))
    if not packages:
        raise SystemExit("dnf completed without producing a dvisvgm RPM")
    for package in packages:
        subprocess.run(
            ["bsdtar", "-xf", str(package), "-C", str(DVISVGM_ROOT)],
            cwd=ROOT,
            check=True,
        )
    if not command_succeeds(["dvisvgm", "--version"]):
        raise SystemExit(
            "The local dvisvgm package was extracted but could not run. "
            "Inspect it with: pixi run dvisvgm --version"
        )


def verify_svg(svg_path: Path) -> None:
    """Reject dvisvgm output that references glyphs without defining them."""
    root = ET.parse(svg_path).getroot()
    defined_ids = {
        element.attrib["id"]
        for element in root.iter()
        if "id" in element.attrib
    }
    href_key = "{http://www.w3.org/1999/xlink}href"
    referenced_ids = {
        element.attrib[href_key][1:]
        for element in root.iter()
        if element.attrib.get(href_key, "").startswith("#")
    }
    missing_ids = sorted(referenced_ids - defined_ids)
    path_count = sum(element.tag.endswith("}path") for element in root.iter())
    if missing_ids or path_count == 0:
        details = ", ".join(missing_ids[:5]) or "no glyph paths"
        raise SystemExit(
            "dvisvgm produced an incomplete SVG ("
            f"{details}). Install Computer Modern/AMS outline fonts and rerun "
            "pixi run prepare-tex."
        )

def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    READY.unlink(missing_ok=True)
    ensure_dvisvgm()
    command = [
        "tectonic",
        "-X",
        "compile",
        "--outfmt",
        "xdv",
        "--keep-logs",
        "--outdir",
        str(OUTPUT),
        str(ROOT / "tools" / "tex-warmup.tex"),
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    subprocess.run(
        [
            "dvisvgm",
            "--no-fonts",
            "--verbosity=0",
            f"--output={OUTPUT / 'tex-warmup.svg'}",
            str(OUTPUT / "tex-warmup.xdv"),
        ],
        cwd=ROOT,
        check=True,
    )
    verify_svg(OUTPUT / "tex-warmup.svg")
    READY.write_text(
        "Tectonic cache and XDV-to-SVG conversion verified for this workspace.\n",
        encoding="utf-8",
    )
    print("TeX toolchain ready; Manim renders now run with cached resources only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
