"""Guard the copied locales/index.ts against upstream drift.

The build replaces upstream's locales/index.ts with our copy (upstream + vi-VN).
If a future base image adds a locale, our copy would silently drop it from the
language menu. This fails the build instead.
"""

import os
import re

LOCALES = "/app/frontend/src/lib/locales"
INDEX = os.path.join(LOCALES, "index.ts")

text = open(INDEX, encoding="utf-8").read()

dirs = {
    d
    for d in os.listdir(LOCALES)
    if os.path.isdir(os.path.join(LOCALES, d))
}

registered = set(re.findall(r"^  '([a-zA-Z]{2}-[a-zA-Z]{2})':", text, flags=re.M))

missing = sorted(dirs - registered)
if missing:
    raise SystemExit(
        f"locales/index.ts is missing upstream locales: {missing} — "
        "update local-sse-fix/vi-lang/locales-index.ts from the new base image"
    )

print("locales registered:", ", ".join(sorted(registered)))
