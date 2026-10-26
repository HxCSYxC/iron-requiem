"""Regenerate the Simplified Chinese strings from the Traditional Chinese ones.

The zh-Hant table in index.html sits between /*HANT*/ and /*END-HANT*/.
This script converts it with OpenCC (Taiwan -> mainland phrasing) and writes
the result between /*HANS*/ and /*END-HANS*/.

    pip install opencc-python-reimplemented
    python tools/make_hans.py index.html
"""
import re
import sys

from opencc import OpenCC

# Words the phrase converter leaves in Taiwan style.
MAINLAND = [('雷射', '激光'), ('吋', '英寸'), ('纪录', '记录')]

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(path, encoding='utf-8').read()
hant = re.search(r'/\*HANT\*/(.*?)/\*END-HANT\*/', src, re.S).group(1)
hans = OpenCC('tw2sp').convert(hant)
for a, b in MAINLAND:
    hans = hans.replace(a, b)
src = re.sub(r'/\*HANS\*/.*?/\*END-HANS\*/', lambda _: '/*HANS*/' + hans + '/*END-HANS*/', src, flags=re.S)
open(path, 'w', encoding='utf-8').write(src)
print(f'Wrote {len(hans)} characters of Simplified Chinese to {path}')
