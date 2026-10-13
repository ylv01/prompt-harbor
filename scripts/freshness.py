"""Report due evidence/source reviews without fetching pages or renewing claims."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/promptharbor/scripts'))
from harbor import audit, load_data, validate


def generate_report(data, today):
    validate(data)
    report = audit(data, today)
    report['sources_due'] = [
        {'id': source['id'], 'url': source['url']}
        for source in data['sources']['sources']
        if (today - date.fromisoformat(source['checked_on'])).days > source['review_days']
    ]
    report['due'] = report['due'] or bool(report['sources_due'])
    return report


def evidence_reason(evidence, data, today):
    source = next(s for s in data['sources']['sources'] if s['id'] == evidence['source_id'])
    policy = data['policy']
    limit = policy['evidence_max_age_days'][evidence['kind']]
    anchors = [('reviewed_on', evidence['reviewed_on'], limit),
               ('source checked_on', source['checked_on'], limit)]
    if evidence['reported_on']:
        anchors.append(('reported_on', evidence['reported_on'], limit))
    if evidence['kind'] == 'community_test':
        anchors.append(('community reviewed_on', evidence['reviewed_on'], policy['community_review_days']))
        community = evidence['community']
        if not evidence['reported_on']:
            anchors.append(('first_seen_on', community['first_seen_on'], policy['undated_community_days']))
        if date.fromisoformat(community['rating']['assessed_on']) > today:
            anchors.append(('assessed_on', community['rating']['assessed_on'], 0))
    reasons = []
    for name, value, days in anchors:
        age = (today - date.fromisoformat(value)).days
        if age < 0:
            reasons.append(f'{name}: future date {value}')
        elif age > days:
            reasons.append(f'{name}: {age} days (limit {days})')
    return '; '.join(reasons)


def markdown_summary(report, data):
    today = date.fromisoformat(report['as_of'])
    sources = {s['id']: s for s in data['sources']['sources']}
    evidence = {e['id']: e for e in data['evidence']['evidence']}
    groups = [
        ('models_needing_refresh', 'Model metadata'),
        ('stale_evidence', 'Expired evidence'),
        ('community_searches_due', 'Community searches'),
        ('prices_needing_refresh', 'Price references'),
        ('sources_due', 'Source reviews'),
    ]
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', '<br>').replace('\r', '')
    lines = ['# Evidence maintenance report', '', f'As of **{today}**.', '',
             '**Review due.**' if report['due'] else '**No reviews due.**', '',
             'This is a maintenance queue, not a code-test failure. Expired records stay in the catalog for historical inspection and are excluded from current recommendations. No dates, claims or validity windows were changed.', '',
             '| Review category | Items |', '|---|---|']
    lines += [f"| {label} | {len(report[key])} |" for key, label in groups]
    if report['stale_evidence']:
        lines += ['', '## Expired evidence', '',
                  '| Record | Model | Reported | Reviewed | Reason | Source |', '|---|---|---|---|---|---|']
        for record_id in report['stale_evidence']:
            ev = evidence[record_id]
            source = sources[ev['source_id']]
            lines.append(f"| `{cell(record_id)}` | `{cell(ev['model_id'])}` | {ev['reported_on'] or 'Unknown'} | {ev['reviewed_on']} | {cell(evidence_reason(ev, data, today))} | [{cell(source['title'])}]({source['url']}) |")
        lines += ['', 'Replace these records with newly evaluated, task-matched evidence when available. Re-reading an old evaluation does not reset its report date; a model may remain eligible through other fresh evidence.']
    for key, label in groups:
        if key == 'stale_evidence' or not report[key]:
            continue
        lines += ['', '## ' + label, '']
        for item in report[key]:
            if key == 'sources_due':
                source = sources[item['id']]
                lines.append(f"- [`{cell(item['id'])}`]({item['url']}) — checked {source['checked_on']}; review interval {source['review_days']} days.")
            else:
                lines.append(f'- `{cell(item)}`')
    lines += ['', 'Review the original sources and deployed model versions before updating the catalog. Missing evidence remains unknown. Use `--fail-due` when a deliberately strict maintenance gate is needed.', '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    parser.add_argument('--fail-due', action='store_true', help='Exit 1 when the maintenance queue is nonempty.')
    parser.add_argument('--output', type=Path, help='Write the JSON report to a file instead of stdout.')
    parser.add_argument('--summary', type=Path, help='Write a readable Markdown maintenance report.')
    parser.add_argument('--github-actions', action='store_true', help='Emit a workflow warning for a nonempty queue.')
    args = parser.parse_args(argv)
    try:
        data = load_data()
        report = generate_report(data, args.as_of)
        text = json.dumps(report, ensure_ascii=True, indent=2) + '\n'
        if args.output:
            args.output.write_text(text, encoding='utf-8')
        else:
            print(text, end='')
        if args.summary:
            args.summary.write_text(markdown_summary(report, data), encoding='utf-8')
        if args.github_actions and report['due']:
            count = sum(len(report[key]) for key in ('models_needing_refresh', 'stale_evidence',
                                                    'community_searches_due', 'prices_needing_refresh', 'sources_due'))
            print(f'::warning title=Evidence review due::{count} maintenance items need review. See the run summary and evidence-review-queue artifact. Expired evidence remains excluded from current recommendations.')
        return 1 if args.fail_due and report['due'] else 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'Freshness report failed: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
