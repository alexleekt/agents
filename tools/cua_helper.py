#!/usr/bin/env python3
"""
cua_helper.py — Python helper for Pi to interact with cua-driver computer-use tools.

Usage:
    from cua_helper import CuaDriver
    driver = CuaDriver()
    apps = driver.list_apps()
    driver.screenshot(window_id=1234, output_path="/tmp/screen.png")
"""

import json
import subprocess
import base64
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass


CUA_DRIVER = "/Applications/CuaDriver.app/Contents/MacOS/cua-driver"


class CuaError(Exception):
    pass


@dataclass
class Window:
    window_id: int
    pid: int
    app_name: str
    title: str


@dataclass
class App:
    pid: int
    name: str
    bundle_id: str
    running: bool
    active: bool


class CuaDriver:
    """Wrapper for cua-driver MCP tools."""

    def __init__(self, driver_path: str = CUA_DRIVER):
        self.driver = driver_path
        if not Path(self.driver).exists():
            raise CuaError(f"CuaDriver not found at {self.driver}")
        self._ensure_daemon()

    def _ensure_daemon(self):
        """Start the cua-driver daemon if not running."""
        result = subprocess.run([self.driver, "status"], capture_output=True, text=True)
        if result.returncode != 0:
            subprocess.run(["open", "-n", "-g", "-a", "CuaDriver", "--args", "serve"],
                           capture_output=True, check=False)
            # Wait for daemon to come up
            for _ in range(10):
                result = subprocess.run([self.driver, "status"], capture_output=True, text=True)
                if result.returncode == 0:
                    break
                import time
                time.sleep(1)

    def _call(self, tool: str, args: Optional[dict] = None) -> dict:
        cmd = [self.driver, "call", tool]
        if args:
            cmd.append(json.dumps(args))
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            stderr = result.stderr.strip()
            raise CuaError(f"cua-driver {tool} failed: {stderr}")
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"raw": result.stdout}

    def check_permissions(self) -> dict:
        """Check TCC permission status."""
        return self._call("check_permissions")

    def get_screen_size(self) -> dict:
        """Get main display size and scale factor."""
        return self._call("get_screen_size")

    def list_apps(self) -> list[App]:
        """List all macOS apps."""
        result = self._call("list_apps")
        apps = result.get("apps", [])
        return [
            App(pid=a["pid"], name=a["name"], bundle_id=a["bundle_id"],
                running=a["running"], active=a.get("active", False))
            for a in apps
        ]

    def list_windows(self) -> list[Window]:
        """List all top-level windows."""
        result = self._call("list_windows")
        windows = result.get("windows", [])
        return [
            Window(window_id=w["window_id"], pid=w["pid"],
                   app_name=w["app_name"], title=w.get("title", ""))
            for w in windows
        ]

    def find_window(self, app_name: Optional[str] = None,
                    bundle_id: Optional[str] = None,
                    title: Optional[str] = None) -> Optional[Window]:
        """Find a window by app name, bundle id, or title substring."""
        windows = self.list_windows()
        for w in windows:
            if app_name and app_name.lower() in w.app_name.lower():
                return w
            if bundle_id and bundle_id.lower() in w.app_name.lower():
                return w
            if title and title.lower() in w.title.lower():
                return w
        return None

    def screenshot(self, window_id: int, format: str = "png",
                   output_path: Optional[str] = None) -> str | bytes:
        """
        Capture a screenshot. Returns base64 string or saves to file if output_path given.
        """
        result = self._call("screenshot", {"window_id": window_id, "format": format})
        # The driver may return base64 image data inside the result
        # For now, return the raw result; caller can extract image data
        if output_path:
            # Try to extract base64 image from result
            raw = json.dumps(result)
            # TODO: Parse actual MCP image content block format
            Path(output_path).write_text(raw)
        return result

    def get_window_state(self, pid: int, window_id: int) -> str:
        """Get UI tree as markdown with element indices."""
        result = self._call("get_window_state", {"pid": pid, "window_id": window_id})
        # The window state is typically returned as text content
        if isinstance(result, dict) and "content" in result:
            return result["content"]
        return json.dumps(result, indent=2)

    def click(self, pid: int, element_index: Optional[int] = None,
              x: Optional[int] = None, y: Optional[int] = None) -> dict:
        """Click at element_index or (x, y) coordinates."""
        args: dict[str, Any] = {"pid": pid}
        if element_index is not None:
            args["element_index"] = element_index
        if x is not None and y is not None:
            args["x"] = x
            args["y"] = y
        return self._call("click", args)

    def double_click(self, pid: int, element_index: int) -> dict:
        return self._call("double_click", {"pid": pid, "element_index": element_index})

    def right_click(self, pid: int, element_index: int) -> dict:
        return self._call("right_click", {"pid": pid, "element_index": element_index})

    def type_text(self, pid: int, text: str) -> dict:
        return self._call("type_text", {"pid": pid, "text": text})

    def press_key(self, pid: int, key: str) -> dict:
        return self._call("press_key", {"pid": pid, "key": key})

    def hotkey(self, pid: int, keys: list[str]) -> dict:
        return self._call("hotkey", {"pid": pid, "keys": keys})

    def scroll(self, pid: int, direction: str = "down", amount: int = 3) -> dict:
        return self._call("scroll", {"pid": pid, "direction": direction, "amount": amount})

    def move_cursor(self, x: int, y: int) -> dict:
        return self._call("move_cursor", {"x": x, "y": y})

    def launch_app(self, bundle_id: str, hidden: bool = False) -> dict:
        return self._call("launch_app", {"bundle_id": bundle_id, "hidden": hidden})

    def drag(self, pid: int, from_x: int, from_y: int, to_x: int, to_y: int) -> dict:
        return self._call("drag", {
            "pid": pid,
            "from_x": from_x, "from_y": from_y,
            "to_x": to_x, "to_y": to_y
        })


if __name__ == "__main__":
    import sys

    driver = CuaDriver()

    if len(sys.argv) < 2:
        print("Usage: cua_helper.py <command> [args...]")
        print("Commands: list-apps, list-windows, screen-size, permissions")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list-apps":
        for app in driver.list_apps():
            status = "✓" if app.running else "○"
            print(f"{status} {app.name} (pid={app.pid}, bundle={app.bundle_id})")
    elif cmd == "list-windows":
        for w in driver.list_windows():
            print(f"window_id={w.window_id} pid={w.pid} app={w.app_name} title={w.title!r}")
    elif cmd == "screen-size":
        print(driver.get_screen_size())
    elif cmd == "permissions":
        print(json.dumps(driver.check_permissions(), indent=2))
    else:
        print(f"Unknown command: {cmd}")
