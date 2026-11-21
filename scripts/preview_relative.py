"""미리보기용: 절대 경로(/...)를 상대 경로로 바꾸고 폴더 주소 뒤에 index.html을 붙인다."""
import os, re, sys, shutil
src, dst = sys.argv[1], sys.argv[2]
shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst, ignore=shutil.ignore_patterns('admin'))
for root, _, files in os.walk(dst):
    for fn in files:
        if not fn.endswith('.html'): continue
        p = os.path.join(root, fn); rel_dir = os.path.relpath(root, dst)
        depth = 0 if rel_dir == '.' else rel_dir.count('/') + 1
        up = '../' * depth or './'
        s = open(p).read()
        def fix(m):
            attr, url = m.group(1), m.group(2)
            if url.startswith('//'): return m.group(0)
            u = url[1:]
            if u == '' or u.endswith('/'): u += 'index.html'
            return f'{attr}="{up}{u}"'
        s = re.sub(r'(href|src)="(/[^"]*)"', fix, s)
        open(p, 'w').write(s)
