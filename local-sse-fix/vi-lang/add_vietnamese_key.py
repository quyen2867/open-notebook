"""Insert `vietnamese: "Tiếng Việt"` into every frontend locale's `common` section.

Runs at image build time (after the vi-VN files are COPYed in). Idempotent:
files that already contain the key are skipped, so rebuilding is safe.
"""
import glob
import re


def add_key(m):
    return m.group(1) + '\n    vietnamese: "Ti\u1ebfng Vi\u1ec7t",'


n = 0
for p in sorted(glob.glob('/app/frontend/src/lib/locales/*/index.ts')):
    txt = open(p, encoding='utf-8').read()
    if 'vietnamese' in txt:
        print('skip:', p)
        continue
    new, cnt = re.subn(r"(?m)^(    turkish: .*,)$", add_key, txt)
    assert cnt == 1, (p, cnt)
    open(p, 'w', encoding='utf-8').write(new)
    n += 1
    print('patched:', p)
print('locales patched:', n)
