from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLATFORM_DIRS = [
    "facebook-activity-logger",
    "x-activity-logger",
    "linkedin-activity-logger",
]


def main() -> int:
    failures = 0
    for platform_dir in PLATFORM_DIRS:
        cwd = REPO_ROOT / platform_dir
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(
            [
                str(REPO_ROOT),
                str(cwd),
                env.get("PYTHONPATH", ""),
            ]
        )
        print(f"\n== {platform_dir} ==")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=cwd,
            env=env,
            check=False,
        )
        if result.returncode:
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
