#!/usr/bin/env python3
"""Serve docs/ like GitHub project Pages (URL prefix /from-prompt-to-prod) and open the browser.

Run from repo root: python3 scripts/serve_site.py
Optional: PORT=9000 python3 scripts/serve_site.py

Regenerate verify HTML after editing the markdown: python3 scripts/build_ghpages.py
"""

from __future__ import annotations

import http.server
import os
import shutil
import socketserver
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
URL_PREFIX = "/from-prompt-to-prod"
DIR_NAME = URL_PREFIX.strip("/")


def main() -> int:
    if not DOCS.is_dir():
        print("Missing docs directory:", DOCS, file=sys.stderr)
        return 1

    try:
        port = int(os.environ.get("PORT", "8765"))
    except ValueError:
        print("PORT must be an integer", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        site_root = Path(tmp) / DIR_NAME
        site_root.mkdir(parents=True)
        for item in DOCS.iterdir():
            dest = site_root / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        os.chdir(tmp)

        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:
                pass

        socketserver.TCPServer.allow_reuse_address = True
        try:
            httpd = socketserver.TCPServer(("", port), QuietHandler)
        except OSError as e:
            print(f"Could not listen on port {port}: {e}", file=sys.stderr)
            return 1

        url = f"http://127.0.0.1:{port}{URL_PREFIX}/"
        print(f"Serving site at {url}")
        print("Press Ctrl+C to stop")

        def open_browser() -> None:
            time.sleep(0.35)
            webbrowser.open(url)

        threading.Thread(target=open_browser, daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
        finally:
            httpd.shutdown()
            httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
