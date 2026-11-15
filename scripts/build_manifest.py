#!/usr/bin/env python3
"""Regenerate MANIFEST.json from bundled sqlite files."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def summarize_sqlite(path: Path) -> dict:
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1"
    )]
    out: dict = {"tables": tables}
    if "bars_5min" in tables:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(bars_5min)")}
        dt = "date_et" if "date_et" in cols else None
        if dt:
            q = f"""
                SELECT symbol, COUNT(*),
                       COUNT(DISTINCT substr({dt}, 1, 10)),
                       MIN(substr({dt}, 1, 10)), MAX(substr({dt}, 1, 10))
                FROM bars_5min GROUP BY symbol ORDER BY symbol
            """
            rows = conn.execute(q).fetchall()
            out["symbols"] = [
                {"symbol": s, "bars": c, "days": d, "from": a, "to": b}
                for s, c, d, a, b in rows
            ]
    if "bars_5m" in tables:
        q = """
            SELECT symbol, COUNT(*),
                   COUNT(DISTINCT substr(datetime, 1, 10)),
                   MIN(substr(datetime, 1, 10)), MAX(substr(datetime, 1, 10))
            FROM bars_5m GROUP BY symbol ORDER BY symbol
        """
        rows = conn.execute(q).fetchall()
        out["symbols"] = [
            {"symbol": s, "bars": c, "days": d, "from": a, "to": b}
            for s, c, d, a, b in rows
        ]
    conn.close()
    return out


def main() -> None:
    manifest: dict = {
        "description": "Canonical bar sqlite snapshots (US + India). One file each, no duplicates.",
        "files": [],
    }
    for path in sorted(DATA.rglob("*.sqlite")):
        rel = path.relative_to(REPO).as_posix()
        entry = {
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        try:
            entry.update(summarize_sqlite(path))
        except sqlite3.Error as exc:
            entry["schema_error"] = str(exc)
        manifest["files"].append(entry)
    out = REPO / "MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(manifest['files'])} files)")


if __name__ == "__main__":
    main()