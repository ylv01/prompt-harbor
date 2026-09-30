"""Check the portable skill, generated docs, local links and release essentials."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/promptharbor/scripts'))
from harbor import load_data, validate
from build_docs import outputs


def check():
    errors=[]
    data=load_data();validate(data)
    locale=data['locale_zh']
    for section,rows,fields in [('tasks',data['taxonomy']['tasks'],('domain','subdomain','label','validation')),
                                ('evidence',data['evidence']['evidence'],('claim','setting','limitations')),
                                ('models',data['models']['models'],('notes',))]:
        translations=locale[section]
        if set(translations)!={row['id'] for row in rows}:
            errors.append('Chinese translation coverage differs from '+section)
        for row in rows:
            required=list(fields)
            if section=='evidence' and row['kind']=='community_test':
                required.append('rating_rationale')
                if row['community'].get('applicability'):required.append('applicability_reason')
            if any(not translations.get(row['id'],{}).get(field) for field in required):
                errors.append('Missing Chinese text: '+row['id'])
    required=['LICENSE','README.md','README.zh-CN.md','CHANGELOG.md','THIRD_PARTY.md',
              'assets/brand/social-preview.png','assets/brand/avatar.png','evals/host-cases.json',
              'skills/promptharbor/assets/logo.svg','skills/promptharbor/assets/avatar.png',
              'examples/library-system/handoffs/manifest.json']
    for name in required:
        if not (ROOT/name).is_file():errors.append('Missing '+name)
    for rel,expected in outputs().items():
        p=ROOT/rel
        if not p.is_file() or p.read_text(encoding='utf-8')!=expected:errors.append('Regenerate '+rel)
    for p in ROOT.rglob('*'):
        if any(x in p.relative_to(ROOT).parts for x in ('.git','out','dist','__pycache__')) or not p.is_file():continue
        if p.suffix=='.svg':
            root=ET.fromstring(p.read_text(encoding='utf-8'))
            if any(n.tag.endswith('script') for n in root.iter()):errors.append('Script in SVG '+str(p))
        if p.suffix=='.json':json.loads(p.read_text(encoding='utf-8'))
        if p.suffix!='.md':continue
        text=p.read_text(encoding='utf-8')
        # Only actual Markdown/HTML links, not path examples in code fences.
        clean=re.sub(r'```.*?```','',text,flags=re.S)
        links=re.findall(r'\]\(([^)]+)\)',clean)+re.findall(r'(?:src|href)="([^"]+)"',clean)
        for link in links:
            if re.match(r'^(https?://|mailto:|#)',link):continue
            link=unquote(link.split('#',1)[0].split('?',1)[0])
            if link and not (p.parent/link).exists():errors.append(f'Broken local link {p.relative_to(ROOT)}: {link}')
        if re.search(r'[CE]:[\\/](Users|PromptHarbor)',text):errors.append('Machine-specific path '+str(p.relative_to(ROOT)))
    skill=(ROOT/'skills/promptharbor/SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\nname: promptharbor\n'):errors.append('Invalid skill frontmatter')
    if len(skill.splitlines())>250:errors.append('Skill entrypoint needs progressive disclosure')
    if errors:raise ValueError('\n'.join(errors))
    return 'Repository checks passed.'


if __name__=='__main__':
    try:print(check())
    except (ValueError,OSError) as exc:
        print(exc,file=sys.stderr);raise SystemExit(1)
