"""Display-only API price references; never consumed by model selection."""
from __future__ import annotations

import math
from datetime import date

from i18n import message


def price_reference(model, sources, policy, today, language='en', context_tokens=None):
    """Describe verified standard uncached USD rates for the requested input size.

    The optional catalog price_reference overrides the legacy single-tier price
    for presentation only. A missing context size shows every recorded tier;
    it never assumes that the cheapest tier applies to an entire long prompt.
    """
    def say(template, **values):
        return message(template, language, **values)

    raw = model.get('price_reference')
    if 'price_reference' not in model:
        legacy = model.get('price_usd_per_million')
        raw = ({'currency': 'USD', 'unit': 'per_million_tokens',
                'source_id': model['source_id'], 'verified_on': model['verified_on'],
                'tiers': [{key: legacy[key] for key in ('max_input_tokens', 'input', 'output')}]}
               if legacy else None)
    result = {'status': 'unknown', 'text': say('Unknown — verify provider pricing'),
              'currency': 'USD', 'unit': 'per_million_tokens', 'tiers': [],
              'source': None, 'context_tokens': context_tokens, 'note': None, 'valid_until': None}
    def finish():
        if result['note']:
            result['text'] += ' · ' + result['note']
        return result
    if not isinstance(raw, dict):
        return finish()
    notes = raw.get('notes', {})
    if isinstance(notes, dict):
        result['note'] = notes.get(language) or notes.get('en')
    result['valid_until'] = raw.get('valid_until')
    source = sources.get(raw.get('source_id'))
    if source:
        result['source'] = {'id': raw.get('source_id'), 'title': source['title'],
                            'url': source['url'], 'verified_on': raw.get('verified_on')}
    if raw.get('currency') != 'USD' or raw.get('unit') != 'per_million_tokens' or not source:
        return finish()
    try:
        age = (today - date.fromisoformat(raw['verified_on'])).days
    except (KeyError, TypeError, ValueError):
        return finish()
    if raw.get('valid_until'):
        try:
            if today > date.fromisoformat(raw['valid_until']):
                result['text'] = say('Unknown — recorded price has expired')
                return finish()
        except (TypeError, ValueError):
            return finish()
    if age < 0 or age > policy['metadata_max_age_days']:
        result['text'] = say('Unknown — price reference needs refresh')
        return finish()
    tiers = raw.get('tiers')
    if not isinstance(tiers, list) or not tiers:
        return finish()
    for tier in tiers:
        if (not isinstance(tier, dict)
                or type(tier.get('max_input_tokens')) is not int or tier['max_input_tokens'] <= 0
                or any(type(tier.get(key)) not in {int, float} or not math.isfinite(tier[key])
                       or tier[key] < 0 for key in ('input', 'output'))):
            return finish()
    tiers = sorted(tiers, key=lambda t: t['max_input_tokens'])
    if len({t['max_input_tokens'] for t in tiers}) != len(tiers):
        return finish()
    if context_tokens is not None:
        selected = next((t for t in tiers if context_tokens <= t['max_input_tokens']), None)
        if selected is None:
            result['text'] = say('Unknown — no verified price for this input length')
            return finish()
        selected_index = tiers.index(selected)
        chosen = [(selected_index, selected)]
    else:
        chosen = list(enumerate(tiers))
    pieces = []
    for index, tier in chosen:
        rates = f"${tier['input']:g} / ${tier['output']:g}"
        lower = tiers[index - 1]['max_input_tokens'] if index else None
        bound = (say('≤{upper} input tokens', upper=f"{tier['max_input_tokens']:,}") if lower is None
                 else say('>{lower}–≤{upper} input tokens', lower=f'{lower:,}', upper=f"{tier['max_input_tokens']:,}"))
        pieces.append(f'{rates} ({bound})')
    result.update(status='available', text='; '.join(pieces), tiers=[dict(tier) for _, tier in chosen])
    return finish()


def price_refresh_due(model, policy, today):
    """Track dated priced records, without treating missing prices as overdue."""
    if 'price_reference' in model:
        raw = model['price_reference']
    else:
        legacy = model.get('price_usd_per_million')
        raw = {'verified_on': model.get('verified_on'), 'tiers': [legacy]} if legacy else None
    if not isinstance(raw, dict) or not raw.get('tiers'):
        return False
    try:
        age = (today - date.fromisoformat(raw['verified_on'])).days
        if not 0 <= age <= policy['metadata_max_age_days']:
            return True
        if raw.get('valid_until') and today > date.fromisoformat(raw['valid_until']):
            return True
    except (KeyError, TypeError, ValueError):
        return True
    return False


def table_cell(value):
    """Preserve a compact Markdown table even for multiline host descriptions."""
    return str(value).replace('|', '\\|').replace('\r\n', '<br>').replace('\n', '<br>').replace('\r', '<br>')


def price_cell(reference, language='en'):
    """A self-contained table cell with source and independent price check date."""
    text = table_cell(reference['text'])
    source = reference.get('source')
    if source:
        text += f"<br>[{message('Price source', language)}]({source['url']})"
        if source.get('verified_on'):
            text += ' · ' + table_cell(source['verified_on'])
    return text


def price_notice(language='en'):
    return message('Price reference: USD per million standard text API input / output tokens, uncached rates. '
                   'Display only; recommendation weights are unchanged. '
                   'Subscriptions, local hosting, audio, images, tools and cache charges are separate.', language)


def shortlist_table(choices, language='en'):
    """Render Top 3 without reordering the recommendations supplied by routing."""
    lines = [message('| Rank | Model | Task fit | Price reference |', language), '|---|---|---|---|']
    for candidate in choices:
        reference = candidate.get('price_reference') or {'text': message('Unknown — verify provider pricing', language)}
        lines.append(f"| {candidate['rank']} | **{table_cell(candidate['name'])}** (`{table_cell(candidate['model_id'])}`) "
                     f"| {table_cell(candidate['reason'])} | {price_cell(reference, language)} |")
    return lines
