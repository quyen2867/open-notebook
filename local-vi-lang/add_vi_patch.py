import glob
import re


def add_key(m):
    return m.group(1) + '\n    vietnamese: "Ti\u1ebfng Vi\u1ec7t",'


# 1. Add `vietnamese` key to every locale's `common` section (after `turkish`)
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

# 2. Add dropdown item to LanguageToggle
p = '/app/frontend/src/components/common/LanguageToggle.tsx'
txt = open(p, encoding='utf-8').read()
assert 'vi-VN' not in txt, 'already patched'
anchor = """        <DropdownMenuItem
          onClick={() => setLanguage('tr-TR')}
          className={currentLang === 'tr-TR' || currentLang.startsWith('tr') ? 'bg-accent' : ''}
        >
          <span>{t('common.turkish')}</span>
        </DropdownMenuItem>"""
assert anchor in txt, 'anchor not found'
item = anchor + """
        <DropdownMenuItem
          onClick={() => setLanguage('vi-VN')}
          className={currentLang === 'vi-VN' || currentLang.startsWith('vi') ? 'bg-accent' : ''}
        >
          <span>{t('common.vietnamese')}</span>
        </DropdownMenuItem>"""
open(p, 'w', encoding='utf-8').write(txt.replace(anchor, item))
print('LanguageToggle patched')
