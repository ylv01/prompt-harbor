"""Regenerate local badges and the explicit task-coverage matrix. Stdlib only."""
import html
import re
import sys
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/promptharbor/scripts'))
from harbor import load_data, validate, community_report


def badge(label,value,color):
    left=max(42,len(label)*7+12);right=len(value)*7+16;width=left+right
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="22" role="img" aria-label="{html.escape(label+' '+value)}">
<title>{html.escape(label+' '+value)}</title>
<clipPath id="r"><rect width="{width}" height="22" rx="3"/></clipPath>
<g clip-path="url(#r)"><path fill="#52616B" d="M0 0h{left}v22H0z"/><path fill="{color}" d="M{left} 0h{right}v22H{left}z"/></g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11">
<text x="{left/2}" y="15">{html.escape(label)}</text><text x="{left+right/2}" y="15">{html.escape(value)}</text></g>
</svg>
'''


def outputs():
    data=load_data();validate(data)
    skill=(ROOT/'skills/promptharbor/SKILL.md').read_text(encoding='utf-8')
    version=re.search(r'version: "([^"]+)"',skill).group(1)
    result={f'skills/promptharbor/{name}':(ROOT/name).read_text(encoding='utf-8')
            for name in ('LICENSE','NOTICE','THIRD_PARTY.md')}
    for name,label,value,color in [('license','license','Apache 2.0','#087F8C'),('version','version',version,'#087F8C'),
                                    ('skill','format','Agent Skill','#087F8C'),('data','model data',data['models']['snapshot_date'],'#527A62')]:
        result['assets/badges/'+name+'.svg']=badge(label,value,color)
    lines=['# Task coverage and gaps','',f"Snapshot: **{data['models']['snapshot_date']}**. Generated from the catalog; not a quality leaderboard.",'',
           f"Catalog: **{len(data['models']['models'])} models · {len(data['taxonomy']['tasks'])} tasks · {len(data['evidence']['evidence'])} evidence records · {len(data['sources']['sources'])} sources**.",'',
           'Direct means a task-mapped measurement, not guaranteed transfer to the user’s prompt.',
           'Capability/proxy includes product support and adjacent-task inference. Missing means no admitted evidence.',
           'All task mappings are editorial judgments. Community reports include signed counterevidence, not just endorsements.','',
           '| Task | Domain / subdomain | Independent measurement | Vendor measurement | Capability / proxy | Community reports |',
           '|---|---|---|---|---|---|']
    evs=data['evidence']['evidence']
    missing=[]
    for task in data['taxonomy']['tasks']:
        i=task['id']
        measured=[e for e in evs if i in e['direct_tasks'] and e['measurement']]
        independent=sorted({e['model_id'] for e in measured if e['kind']=='independent_eval'})
        vendor=sorted({e['model_id'] for e in measured if e['kind']=='vendor_eval'})
        proxy=sorted({e['model_id'] for e in evs if e['kind']!='community_test' and (i in e['proxy_tasks'] or i in e['direct_tasks'] and not e['measurement'])})
        community=sorted({e['model_id']+' ('+e['community']['stance']+')' for e in evs if e['kind']=='community_test' and i in e['direct_tasks']+e['proxy_tasks']})
        if not independent and not vendor and not proxy and not community:missing.append(i)
        lines.append(f"| `{i}` | {task['domain']} / {task['subdomain']} | {', '.join(independent) or '—'} | {', '.join(vendor) or '—'} | {', '.join(proxy) or '—'} | {', '.join(community) or '—'} |")
    lines += ['', '## Explicit gaps', '', ', '.join(f'`{i}`' for i in missing), '',
              'These tasks are recognizable even when the catalog cannot establish a winner. Research live evidence, retain a feasible current model as a baseline, or propose a task trial.', '',
              '## Admitted sources', '']
    for source in data['sources']['sources']:
        lines.append(f"- [{source['title']}]({source['url']}) — {source['publisher']}; checked {source['checked_on']}; publication {source['published_on'] or 'not established'}.")
    result['docs/COVERAGE.md']='\n'.join(lines)+'\n'
    report=community_report(data,date.fromisoformat(data['models']['snapshot_date']))
    sources={s['id']:s for s in data['sources']['sources']}
    evidence={e['id']:e for e in evs}
    lines=['# Community task ratings','',f"Reviewed: **{report['as_of']}**. All **{len(report['models'])}** catalog models were searched.",'',
           'Scores are PromptHarbor editorial judgments of specific reported outcomes, on a 0–10 scale. They are not benchmark measurements or global model ratings.',
           'Unknown task ratings remain unknown. A **proxy** label means only adjacent-task reports support that rating; it is not a direct observation of that task.',
           'Confidence reflects corroboration and evidence quality; same-origin reposts do not add votes.',
           'See the [rating rubric and weighting rules](../skills/promptharbor/references/community.md).','',
           '| Model | Task ratings (0–10) | Distinct report origins |', '|---|---|---|']
    for m in report['models']:
        rows=[evidence[i] for i in m['research']['evidence_ids']]
        ratings='; '.join(f"`{t['task']}` **{t['score']}**"+(' (proxy)' if t['mapping']=='proxy' else '') for t in m['tasks']) or 'No admitted task reports'
        lines.append(f"| {m['name']} | {ratings} | {len({e['community']['origin_id'] for e in rows})} |")
    for m in report['models']:
        lines += ['',f"## {m['name']}",'',f"Search: {m['research']['searched_on']} · status: {m['research']['status']}",'',
                  'Queries: '+ '; '.join('`'+q.replace('`','')+'`' for q in m['research']['queries']), '']
        for t in m['tasks']:
            lines.append(f"- `{t['task']}`: **{t['score']}/10**, {t['confidence']} confidence, {t['mapping']} mapping, {t['origin_count']} origin(s).")
        for eid in m['research']['evidence_ids']:
            e=evidence[eid]; c=e['community']; s=sources[e['source_id']]; r=c['rating']
            tasks=', '.join('`'+t+'`' for t in e['direct_tasks']) or 'None (adjacent task only)'
            proxies=', '.join('`'+t+'`' for t in e['proxy_tasks']) or 'None'
            lines += ['',f"### [{s['title']}]({s['url']})",'',
                      f"**{r['value']}/10** · {c['stance']} · {c['grade']} · {r['confidence']} confidence. Author: {c['author']}.",
                      f"Reported: {e['reported_on'] or 'absolute date unknown'} · first seen: {c['first_seen_on']} · assessed: {r['assessed_on']}.",
                      f"Direct tasks: {tasks}. Proxy tasks: {proxies}.",'',e['claim'],'',
                      '**Rating reason:** '+r['rationale'],'','**Limits:** '+e['limitations']]
            if c.get('applicability'):
                a=c['applicability']; fix=sources[a['source_id']]
                lines += ['',f"**Current-revision relevance:** {a['weight']} ×. {a['reason']} [Update source]({fix['url']})."]
            if c['artifact_urls']:
                lines += ['', 'Artifacts: '+', '.join(f"[artifact {i}]({url})" for i,url in enumerate(c['artifact_urls'],1))+'.']
    result['docs/COMMUNITY.md']='\n'.join(lines)+'\n'
    return result


if __name__=='__main__':
    for path,content in outputs().items():
        target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8')
    print('Regenerated badges, coverage and community ratings.')
