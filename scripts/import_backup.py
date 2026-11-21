"""백업(docs.json)에서 사이트 콘텐츠를 만든다. 한 번만 쓰는 이관 스크립트."""
import json, re, os, sys, csv
D = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
def w(path, front, body=''):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    import yaml
    with open(p, 'w') as f:
        f.write('---\n' + yaml.safe_dump(front, allow_unicode=True, sort_keys=False) + '---\n\n' + body.strip() + '\n')
def clean(md):
    md = re.sub(r'xml:namespace prefix[^\n/]*/', '', md)
    md = re.sub(r'\[!\[\]\([^)]*\)\]\([^)]*\)', '', md)
    md = re.sub(r'\[\]\([^)]*\)', '', md)
    md = re.sub(r'\(http://www\.scripta\.kr/scripta_v0010/\?module=file[^)]*\)', '(#)', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()
def safe(name):
    base, ext = os.path.splitext(name)
    base = re.sub(r'[^0-9A-Za-z가-힣._-]+', '_', base).strip('_') or 'file'
    return base + ext.lower()
manifest = []
def fileref(srl, f, folder):
    src, up, size = f
    dest = f'/files/{folder}/{safe(src)}'
    manifest.append([srl, src, up, dest, size])
    return dest

# --- journal ---
vols = {1:'817',2:'825',3:'833',4:'842',5:'144525',6:'144537',7:'144545',8:'144552',9:'144850',10:'145208',11:'146318'}
for v, s in vols.items():
    d = D[s]
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', d['title'])
    month, year = (m.group(1), m.group(2)) if m else ('October', '2020')
    pdfs = [f for f in d['files'] if f[0].lower().endswith('.pdf')]
    # 각 PDF 링크 바로 앞의 글(저자·제목)을 그 PDF와 짝짓는다
    norm = lambda x: x.replace('\\_', '_').replace('&amp;', '&').strip()
    byname = {norm(f[0]): f for f in pdfs}
    arts = []; used = set(); last = 0; md = d['md']
    for m in re.finditer(r'\[\[([^\]]+?\.pdf)\]\(', md):
        blk = md[last:m.start()]; last = m.end()
        f = byname.get(norm(m.group(1)))
        if not f or f[0] in used: continue
        used.add(f[0])
        lines = [l.strip() for l in blk.split('\n') if l.strip() and not l.strip().startswith(('[', ']', ')')) and not l.strip().startswith('http')]
        lines = [re.sub(r'^\S*\)\s*\]?$', '', l) for l in lines]; lines = [l for l in lines if l]
        author = ''; title = []
        for l in lines:
            if re.fullmatch(r'\*[^*]+\*.*', l) and not author: author = l.replace('*', '').strip()
            elif author: title.append(l.replace('*', '').strip())
        kind = 'front' if re.search(r'Cover|Contents', author + f[0], re.I) else 'article'
        arts.append({'kind': kind, 'author': '' if kind == 'front' else author, 'title': (author if kind == 'front' else ' '.join(title)) or f[0], 'pdf': fileref(s, f, f'journal/vol{v:02d}')})
    for f in pdfs:
        if f[0] not in used:
            arts.append({'kind': 'article', 'author': '', 'title': norm(f[0]), 'pdf': fileref(s, f, f'journal/vol{v:02d}')})
    front = {'volume': v, 'year': int(year), 'month': month, 'date': f'{year}-10-01', 'articles': arts}
    body = '' if arts else '이 호의 논문 목록과 PDF는 아직 올라오지 않았습니다.'
    w(f'scripta/vol-{v:02d}.md', front, body)

# --- conferences ---
conf = [('1124','854','2007-10-09','domestic'),('1129','860','2008-10-01','international'),('1132','873','2009-10-01','domestic'),
        ('1143','882','2010-10-01','international'),('1153','893','2011-10-01','international'),('1178','903','2012-06-01','domestic'),
        ('1196','912','2012-10-01','international'),('144562','144565','2013-06-01','domestic'),('144559','144568','2013-10-01','international'),
        ('144615','144664','2014-06-01','domestic'),('144617','144624','2014-10-01','international'),('144619','144633','2015-06-01','domestic'),
        ('144621','144642','2015-10-01','international'),('144709','144649','2016-06-01','domestic'),('144714','144657','2016-10-01','international'),
        ('145415',None,'2021-05-29','domestic'),('145466',None,'2021-12-18','international'),('146641',None,'2026-01-13','international')]
for c, p, date, kind in conf:
    d = D[c]
    title = re.sub(r'\s*안내\(zoom온라인 회의\)', ' (Zoom 온라인)', d['title']).strip()
    files = []
    if p:
        for f in D[p]['files']:
            files.append({'label': os.path.splitext(f[0])[0], 'file': fileref(p, f, f'conferences/{date[:4]}-{kind}')})
    for f in d['files']:
        files.append({'label': os.path.splitext(f[0])[0], 'file': fileref(c, f, f'conferences/{date[:4]}-{kind}')})
    slug = f'{date[:4]}-{kind}'
    w(f'conferences/{slug}.md', {'title': title, 'date': date, 'kind': kind, 'files': files}, clean(d['md']))

# --- notices ---
notes = [('310','2008-12-16'),('750','2009-10-10'),('756','2009-11-02'),('758','2009-12-22'),('765','2013-03-19'),('146641','2026-01-10')]
for s, date in notes:
    d = D[s]
    title = re.sub(r'\s*\(\d{4}\.\d{1,2}\.\d{1,2}\.? ?게시\)', '', d['title']).strip()
    files = [{'label': f[0], 'file': fileref(s, f, 'notices')} for f in d['files']]
    w(f'notices/{date}-{s}.md', {'title': title, 'date': date, 'files': files}, clean(d['md']))

# --- pages ---
pages = {'ko/history.md': ('250', '설립 목적과 연혁'), 'ko/bylaws.md': ('326', '정관(회칙)'), 'ko/join.md': ('256', '입회 안내'),
         'ko/scripta-about.md': ('264', '학술지 SCRIPTA'), 'ko/submission.md': ('269', '논문 투고 안내'),
         'en/history.md': ('946', 'Mission and History'), 'en/membership.md': ('952', 'Membership'),
         'en/scripta-about.md': ('136', 'SCRIPTA'), 'en/submission.md': ('150', 'Submission Guidelines')}
for path, (s, t) in pages.items():
    d = D[s]
    files = [{'label': f[0], 'file': fileref(s, f, 'forms' if 'join' in path or 'membership' in path else 'pages')} for f in d['files']]
    w(f'pages/{path}', {'title': t, 'files': files}, clean(d['md']))

with open(os.path.join(OUT, '..', 'scripts', 'pdf-manifest.csv'), 'w', newline='') as f:
    cw = csv.writer(f); cw.writerow(['document_srl', 'original_name', 'backup_path', 'site_path', 'bytes']); cw.writerows(manifest)
print(len(manifest), 'files in manifest')
