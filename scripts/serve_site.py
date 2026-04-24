#!/usr/bin/env python3
"""Serve docs/ like GitHub project Pages (URL prefix /from-prompt-to-prod) and open the browser.

Reads from repo docs/ on every request (no copy) — save CSS/HTML and refresh the browser.

Run from repo root: python3 scripts/serve_site.py
Optional: PORT=9000 python3 scripts/serve_site.py

Regenerate self-audit HTML after editing the markdown: python3 scripts/build_ghpages.py
"""

from __future__ import annotations

import http.server
import os
import socketserver
import sys
import threading
import time
import webbrowser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
URL_PREFIX = "/from-prompt-to-prod"


def make_handler(docs: Path) -> type[http.server.SimpleHTTPRequestHandler]:
    class GHPagesRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(docs), **kwargs)

        def log_message(self, format: str, *args: object) -> None:
            pass

        def end_headers(self) -> None:
            # Dev: avoid stale assets without hard-refresh (optional)
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def translate_path(self, path: str) -> str:
            clean = unquote(urlparse(path).path)
            if "?" in clean:
                clean = clean.split("?", 1)[0]
            clean = clean.rstrip("/")
            pfx = URL_PREFIX
            if clean == pfx or clean == "" or clean == "/":
                rel = Path("index.html")
            elif clean.startswith(pfx + "/"):
                rest = clean[len(pfx) + 1 :]
                rel = Path(rest) if rest else Path("index.html")
            else:
                return super().translate_path(path)
            # resolve under docs, prevent escape
            try:
                full = (docs / rel).resolve()
            except OSError:
                return str(docs / "index.html")
            if not str(full).startswith(str(docs.resolve())):
                return str(docs / "index.html")
            if full.is_file():
                return str(full)
            if full.is_dir() and (full / "index.html").is_file():
                return str(full / "index.html")
            if not rel.suffix and (docs / rel / "index.html").is_file():
                return str((docs / rel / "index.html").resolve())
            return str(full)

    return GHPagesRequestHandler


def main() -> int:
    if not DOCS.is_dir():
        print("Missing docs directory:", DOCS, file=sys.stderr)
        return 1

    try:
        port = int(os.environ.get("PORT", "8765"))
    except ValueError:
        print("PORT must be an integer", file=sys.stderr)
        return 1

    os.chdir(ROOT)  # stable cwd; paths use absolute DOCS
    handler = make_handler(DOCS)
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("", port), handler)
    except OSError as e:
        print(f"Could not listen on port {port}: {e}", file=sys.stderr)
        return 1

    url = f"http://127.0.0.1:{port}{URL_PREFIX}/"
    print(f"Serving live from {DOCS} at {url}")
    print("Edits to docs/ show up on browser refresh; Press Ctrl+C to stop")

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
