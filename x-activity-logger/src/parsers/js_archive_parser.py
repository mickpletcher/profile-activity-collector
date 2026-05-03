from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ASSIGNMENT_RE = re.compile(r"^[\w\.]+\s*=\s*", re.MULTILINE)


def parse_js_archive_file(path: Path) -> Any:
    """Parse X archive .js files that store JSON via window.YTD.* assignments."""
    raw = path.read_text(encoding="utf-8")
    raw = raw.strip().rstrip(";")
    cleaned = ASSIGNMENT_RE.sub("", raw, count=1)
    return json.loads(cleaned)
