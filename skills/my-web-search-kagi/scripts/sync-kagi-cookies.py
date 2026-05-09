#!/usr/bin/env python3
"""
Sync Kagi cookies from Firefox/Zen/LibreWolf/etc to agent-browser Chrome session.

Usage:
    python3 sync-kagi-cookies.py [--browser zen|firefox|librewolf|waterfox|floorp]

This script:
    1. Finds the default Firefox-variant profile
    2. Copies cookies.sqlite (to avoid database lock)
    3. Extracts Kagi cookies
    4. Injects them into agent-browser via CDP cookies API
"""

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


def find_profile_dir(browser_name: str) -> Path | None:
    """Find the default profile directory for a Firefox-variant browser."""
    home = Path.home()

    # Platform-specific paths
    if sys.platform == "darwin":
        base_dirs = [
            home / "Library" / "Application Support" / browser_name / "Profiles",
            home / "Library" / "Application Support" / "Firefox" / "Profiles",
        ]
    elif sys.platform == "linux":
        base_dirs = [
            home / ".mozilla" / browser_name / "Profiles",
            home / ".var" / "app" / f"org.{browser_name}.Browser" / "data" / browser_name / "Profiles",
            home / ".mozilla" / "firefox" / "Profiles",
        ]
    else:
        base_dirs = []

    for base in base_dirs:
        if not base.exists():
            continue

        # Find the default-release profile (or any profile with cookies.sqlite)
        for profile in base.iterdir():
            if profile.is_dir() and (profile / "cookies.sqlite").exists():
                # Prefer default-release profiles
                if "default" in profile.name.lower() or "release" in profile.name.lower():
                    return profile

        # Fallback: any profile with cookies
        for profile in base.iterdir():
            if profile.is_dir() and (profile / "cookies.sqlite").exists():
                return profile

    return None


def extract_kagi_cookies(profile_dir: Path) -> list[dict]:
    """Extract Kagi cookies from a Firefox profile's cookies.sqlite."""
    src = profile_dir / "cookies.sqlite"
    if not src.exists():
        raise FileNotFoundError(f"No cookies.sqlite found in {profile_dir}")

    # Copy to temp to avoid database lock while browser is running
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    shutil.copy2(src, tmp_path)

    try:
        conn = sqlite3.connect(tmp_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name, value, host, path, expiry, isSecure, isHttpOnly, sameSite
            FROM moz_cookies
            WHERE host LIKE '%kagi%'
            """
        )

        cookies = []
        for row in cur.fetchall():
            # Firefox sameSite: 0=None, 1=Lax, 2=Strict
            same_site_map = {0: "None", 1: "Lax", 2: "Strict"}
            cookies.append({
                "name": row["name"],
                "value": row["value"],
                "domain": row["host"],
                "path": row["path"],
                "expires": row["expiry"] // 1000 if row["expiry"] else None,  # ms → s
                "secure": bool(row["isSecure"]),
                "httpOnly": bool(row["isHttpOnly"]),
                "sameSite": same_site_map.get(row["sameSite"], "Lax"),
            })

        conn.close()
        return cookies
    finally:
        tmp_path.unlink(missing_ok=True)


def inject_into_agent_browser(cookies: list[dict]) -> None:
    """Inject cookies into agent-browser via the cookies set command."""
    if not cookies:
        print("No Kagi cookies found. Are you logged into Kagi in your Firefox-variant browser?")
        sys.exit(1)

    for c in cookies:
        cmd = [
            "agent-browser", "cookies", "set",
            c["name"], c["value"],
            "--domain", c["domain"],
            "--path", c["path"],
        ]
        if c.get("secure"):
            cmd.append("--secure")
        if c.get("httpOnly"):
            cmd.append("--httpOnly")
        if c.get("sameSite"):
            cmd.extend(["--sameSite", c["sameSite"]])
        if c.get("expires"):
            cmd.extend(["--expires", str(c["expires"])])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Fallback to npx
            cmd[0] = "npx"
            cmd.insert(1, "agent-browser")
            result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Failed to set cookie {c['name']}: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        print(f"  ✓ {c['name']} ({c['domain']})")

    print(f"\nInjected {len(cookies)} Kagi cookie(s) into agent-browser.")


def main():
    parser = argparse.ArgumentParser(
        description="Sync Kagi cookies from Firefox-variant browser to agent-browser"
    )
    parser.add_argument(
        "--browser",
        default="zen",
        choices=["zen", "firefox", "librewolf", "waterfox", "floorp", "palemoon"],
        help="Firefox-variant browser name (default: zen)",
    )
    args = parser.parse_args()

    print(f"Looking for {args.browser} profile...")
    profile = find_profile_dir(args.browser)

    if not profile:
        print(f"Could not find a {args.browser} profile with cookies.sqlite.", file=sys.stderr)
        print("Make sure your browser is installed and has been used to visit Kagi.", file=sys.stderr)
        sys.exit(1)

    print(f"Found profile: {profile}")
    print("Extracting Kagi cookies...")

    cookies = extract_kagi_cookies(profile)
    print(f"Found {len(cookies)} Kagi cookie(s)")

    print("Injecting into agent-browser...")
    inject_into_agent_browser(cookies)
    print("\nYou can now search Kagi via agent-browser without CAPTCHA.")


if __name__ == "__main__":
    main()
