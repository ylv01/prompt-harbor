"""Evidence retrieval and conservative model shortlisting. Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path
from i18n import catalog_text, message, resolve_language
from price import price_cell, price_notice, price_reference, price_refresh_due, shortlist_table

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"independent_eval", "vendor_eval", "official_capability", "community_test"}
MODALITIES = {"text", "image", "video", "audio"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def load_data(root=ROOT):
    data = {name: read_json(root / "data" / f"{name}.json")
            for name in ("taxonomy", "models", "sources", "evidence", "policy", "community_research")}
    data['locale_zh'] = read_json(root / 'data/locales/zh-CN.json')
    return data


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(rows, label):
    ids = [row["id"] for row in rows]
    require(len(ids) == len(set(ids)), f"Duplicate {label} id")
    return set(ids)


def iso(value):
    return date.fromisoformat(value)


def validate(data):
    """Cross-file referential and semantic validation, also used before every query."""
    tasks = unique(data["taxonomy"]["tasks"], "task")
    models = unique(data["models"]["models"], "model")
    sources = unique(data["sources"]["sources"], "source")
    unique(data["evidence"]["evidence"], "evidence")
    for section in data.values():
        require(section["schema_version"] == 1, "Unsupported schema version")
    snapshot = iso(data["models"]["snapshot_date"])
    ranking = data["policy"]["ranking"]
    for weight in [ranking["default_community_weight"], *ranking["task_community_weights"].values()]:
        require(type(weight) in {int, float} and 0 <= weight <= 0.4, "Invalid community weight")
    require(set(ranking["task_community_weights"]) <= tasks, "Unknown weighted task")
    for task in data["taxonomy"]["tasks"]:
        require(all(task.get(k) for k in ("domain", "subdomain", "label", "description", "validation")),
                f"Incomplete task {task['id']}")
        for pattern in task["patterns"]:
            re.compile(pattern)
    for source in data["sources"]["sources"]:
        require(source["url"].startswith("https://"), "Sources require HTTPS")
        require(iso(source["checked_on"]) <= snapshot, "Source check after snapshot")
        if source["published_on"]:
            require(iso(source["published_on"]) <= iso(source["checked_on"]), "Future source")
    for model in data["models"]["models"]:
        require(model["source_id"] in sources, f"Unknown model source: {model['id']}")
        require(set(model["input_modalities"]) <= MODALITIES, "Invalid modality")
        require(model["status"] in {"available", "preview", "retired"}, "Invalid lifecycle")
        require(type(model["open_weights"]) is bool, "open_weights must be boolean")
        require(model["context_tokens"] is None or type(model["context_tokens"]) is int
                and model["context_tokens"] > 0, "Invalid context")
        require(iso(model["verified_on"]) <= snapshot, "Future model metadata")
    for ev in data["evidence"]["evidence"]:
        require(ev["model_id"] in models and ev["source_id"] in sources, f"Broken evidence link: {ev['id']}")
        require(ev["kind"] in KINDS, "Invalid evidence kind")
        require(ev["direct_tasks"] or ev["proxy_tasks"], "Evidence without task mapping")
        require(set(ev["direct_tasks"] + ev["proxy_tasks"]) <= tasks, "Unknown evidence task")
        require(not (set(ev["direct_tasks"]) & set(ev["proxy_tasks"])), "Ambiguous task mapping")
        require(all(ev.get(k) for k in ("claim", "limitations", "setting")), "Missing evidence context")
        require(iso(ev["reviewed_on"]) <= snapshot, "Future review")
        if ev["reported_on"]:
            require(iso(ev["reported_on"]) <= iso(ev["reviewed_on"]), "Future result")
        measurement = ev["measurement"]
        if measurement:
            require(ev["kind"] in {"independent_eval", "vendor_eval", "community_test"}, "Capability is not a measurement")
            require(type(measurement["value"]) in {int, float} and math.isfinite(measurement["value"]), "Invalid score")
            require(all(measurement.get(k) for k in ("benchmark", "version", "metric", "unit", "protocol")), "Incomplete measurement")
        if ev.get("comparison_group"):
            require(measurement is not None, "Comparison requires measurement")
        if ev["kind"] == "community_test":
            c = ev.get("community", {})
            require(c.get("origin_id") and c.get("author"), "Community evidence needs its independent origin and author")
            require(c.get("grade") in {"reproduced", "artifact_report", "firsthand"}, "Invalid community grade")
            require(c.get("stance") in {"positive", "negative", "mixed"}, "Invalid community stance")
            require(iso(c["first_seen_on"]) <= iso(ev["reviewed_on"]), "Invalid community first-seen date")
            require(isinstance(c.get("artifact_urls"), list) and all(u.startswith("https://") for u in c["artifact_urls"]), "Invalid artifact URLs")
            require(c["grade"] == "firsthand" or c["artifact_urls"], "Artifact evidence needs public artifacts")
            require(c["grade"] != "reproduced" or c.get("reproduction_url", "").startswith("https://"), "Reproduced means a documented independent rerun")
            rating = c.get('rating', {})
            require(type(rating.get('value')) in {int, float} and 0 <= rating['value'] <= 10, 'Community rating must be 0–10')
            require(rating.get('rationale') and rating.get('confidence') in {'low', 'medium', 'high'}, 'Community rating needs a reason and confidence')
            require(iso(rating['assessed_on']) <= snapshot, 'Future community assessment')
            applicability = c.get('applicability')
            if applicability:
                require(type(applicability.get('weight')) in {int, float} and 0 < applicability['weight'] <= 1,
                        'Invalid community revision applicability')
                require(applicability.get('reason') and applicability.get('source_id') in sources,
                        'Revision applicability needs a reason and source')
    groups = {}
    for ev in data["evidence"]["evidence"]:
        group = ev.get("comparison_group")
        if group:
            m = ev["measurement"]
            key = (ev["source_id"], m["benchmark"], m["version"], m["metric"], m["unit"], m["protocol"])
            require(group not in groups or groups[group] == key, "Incompatible comparison group")
            groups[group] = key
    researched = unique(data['community_research']['models'], 'community research model')
    require(researched == models, 'Community research must cover every catalog model')
    evidence_ids = {e['id']: e for e in data['evidence']['evidence']}
    for row in data['community_research']['models']:
        require(row.get('queries') and row.get('summary'), 'Community research needs queries and a summary')
        require(iso(row['searched_on']) <= snapshot, 'Future community search')
        require(row['status'] in {'reviewed', 'no_specific_reports'}, 'Invalid community research status')
        for evidence_id in row['evidence_ids']:
            ev = evidence_ids.get(evidence_id)
            require(ev and ev['model_id'] == row['id'] and ev['kind'] == 'community_test', 'Broken community research evidence link')
    return True


def classify(prompt, data):
    """Conservative bilingual lexical fallback; semantic interpretation belongs to the host."""
    require(isinstance(prompt, str) and prompt.strip(), "Prompt must not be empty")
    matches = []
    for task in data["taxonomy"]["tasks"]:
        hits = [p for p in task["patterns"] if re.search(p, prompt, re.I)]
        if hits:
            matches.append((len(hits), task["id"]))
    matches.sort(key=lambda x: (-x[0], x[1]))
    ids = [t for _, t in matches[:4]] or ["general.everyday"]
    return {"tasks": ids, "classification_method": "lexical_fallback",
            "classification_confidence": "low", "prompt": prompt,
            "notes": ["Host should verify intent, negation, attachments, constraints and mixed tasks."]}


def validate_job(job, data):
    allowed = {"tasks", "prompt", "classification_method", "classification_confidence", "notes",
               "current_model", "available_models", "input_modalities", "context_tokens", "tools_required",
               "open_weights_only", "allow_preview", "priority", "max_input_price", "max_output_price", "community_weight", "language"}
    require(isinstance(job, dict) and not set(job) - allowed, "Unknown job field")
    resolve_language(job.get('language'))
    tasks = {t["id"] for t in data["taxonomy"]["tasks"]}
    require(isinstance(job.get("tasks"), list) and 0 < len(job["tasks"]) <= 6, "Provide 1–6 task IDs")
    require(all(isinstance(t, str) for t in job["tasks"]) and set(job["tasks"]) <= tasks, "Unknown task ID")
    require(len(job["tasks"]) == len(set(job["tasks"])), "Duplicate task ID")
    for key in ("tools_required", "open_weights_only", "allow_preview"):
        require(key not in job or type(job[key]) is bool, f"{key} must be boolean")
    for key in ("context_tokens", "max_input_price", "max_output_price"):
        if key in job:
            require(type(job[key]) in {int, float} and math.isfinite(job[key]) and job[key] >= 0,
                    f"{key} must be a nonnegative finite number")
    if "context_tokens" in job:
        require(type(job["context_tokens"]) is int, "context_tokens must be an integer")
    require(job.get("priority", "quality") in {"quality", "cost", "latency"}, "Invalid priority")
    modalities = job.get("input_modalities", ["text"])
    require(isinstance(modalities, list) and all(isinstance(x, str) for x in modalities)
            and set(modalities) <= MODALITIES, "Invalid input modalities")
    available = job.get("available_models")
    require(available is None or isinstance(available, list) and all(isinstance(x, str) for x in available),
            "available_models must be an array of exact model IDs")
    if "current_model" in job:
        require(isinstance(job["current_model"], str), "current_model must be an exact model ID")
    if "community_weight" in job:
        require(type(job["community_weight"]) in {int, float} and 0 <= job["community_weight"] <= 0.4,
                "community_weight must be between 0 and 0.4")
    return job


def age_in_days(value, today):
    return (today - iso(value)).days


def evidence_fresh(ev, data, today):
    policy = data["policy"]
    sources = {s["id"]: s for s in data["sources"]["sources"]}
    source = sources[ev["source_id"]]
    # Re-reading an old benchmark does not turn it into a new evaluation.
    anchors = [ev["reviewed_on"], source["checked_on"]]
    if ev["reported_on"]:
        anchors.append(ev["reported_on"])
    if ev["kind"] == "community_test":
        if iso(ev['community']['rating']['assessed_on']) > today:
            return False
        if not 0 <= age_in_days(ev["reviewed_on"], today) <= policy["community_review_days"]:
            return False
        if not ev["reported_on"] and not 0 <= age_in_days(ev["community"]["first_seen_on"], today) <= policy["undated_community_days"]:
            return False
    return all(0 <= age_in_days(a, today) <= policy["evidence_max_age_days"][ev["kind"]] for a in anchors)


def eligibility(model, job, data, today):
    reasons = []
    source = next(s for s in data["sources"]["sources"] if s["id"] == model["source_id"])
    ttl = data["policy"]["metadata_max_age_days"]
    if any(not 0 <= age_in_days(d, today) <= ttl for d in (model["verified_on"], source["checked_on"])):
        reasons.append("metadata_needs_refresh")
    if model["status"] == "retired" or model["status"] == "preview" and not job.get("allow_preview", False):
        reasons.append("unavailable_or_preview")
    if "available_models" in job and model["id"] not in job["available_models"]:
        reasons.append("outside_available_models")
    if not set(job.get("input_modalities", ["text"])) <= set(model["input_modalities"]):
        reasons.append("input_modality_not_verified")
    if job.get("context_tokens", 0) and (model["context_tokens"] is None or model["context_tokens"] < job["context_tokens"]):
        reasons.append("context_too_small_or_unknown")
    if job.get("tools_required") and model["tool_calling"] is not True:
        reasons.append("tools_not_verified")
    if job.get("open_weights_only") and not model["open_weights"]:
        reasons.append("closed_weights")
    for side in ("input", "output"):
        cap = job.get(f"max_{side}_price")
        if cap is not None:
            price = model["price_usd_per_million"]
            # Only standard short-context rates are represented in the seed dataset.
            if price is None or job.get("context_tokens", 0) > price["max_input_tokens"]:
                reasons.append(f"{side}_price_unknown_for_request")
            elif price[side] > cap:
                reasons.append(f"{side}_price_over_budget")
    return reasons


def comparable_pairs(a, b):
    pairs = []
    for ea in a:
        for eb in b:
            if ea.get("comparison_group") and ea["comparison_group"] == eb.get("comparison_group"):
                pairs.append((ea, eb))
    return pairs


def community_assessment(rows, task, today):
    """Weighted editorial score for one model/task, with one vote per origin."""
    origins = {}
    mappings = set()
    for ev in rows:
        if ev['kind'] != 'community_test':
            continue
        if iso(ev['community']['rating']['assessed_on']) > today:
            continue
        match = 1 if task in ev['direct_tasks'] else 0.45 if task in ev['proxy_tasks'] else 0
        if not match:
            continue
        mappings.add('direct' if task in ev['direct_tasks'] else 'proxy')
        c = ev['community']
        quality = {'reproduced': 1, 'artifact_report': 0.6, 'firsthand': 0.2}[c['grade']]
        freshness = 0.5 ** (age_in_days(ev['reported_on'], today)/60) if ev['reported_on'] else 0.5
        applicability = c.get('applicability', {}).get('weight', 1)
        reliability = quality * match * freshness * applicability
        score = c['rating']['value']
        signal = (score - 5)/5 * reliability
        origin = origins.setdefault(c['origin_id'], {'observations': set(), 'evidence_ids': []})
        # Repeated URLs, reposts and copied records do not multiply a judgment.
        origin['observations'].add((score, reliability, signal))
        origin['evidence_ids'].append(ev['id'])
    assessments = []
    for origin_id, value in sorted(origins.items()):
        obs = value['observations']
        total = sum(o[1] for o in obs)
        assessments.append({'origin_id': origin_id, 'score': sum(o[0]*o[1] for o in obs)/total,
                            'reliability': max(o[1] for o in obs),
                            'signal': sum(o[2] for o in obs)/len(obs), 'evidence_ids': value['evidence_ids']})
    weight = sum(o['reliability'] for o in assessments)
    score = round(sum(o['score']*o['reliability'] for o in assessments)/weight, 1) if weight else None
    signal = sum(o['signal'] for o in assessments)/max(3, len(assessments))
    confidence = 'insufficient' if not assessments else 'low'
    if len(assessments) >= 3 and sum(o['reliability'] >= 0.3 for o in assessments) >= 2:
        confidence = 'medium'
    return {'score': score, 'scale': 10, 'confidence': confidence, 'signal': round(signal, 6),
            'mapping': 'direct_and_proxy' if len(mappings) == 2 else next(iter(mappings), 'none'),
            'origins': [{**o, 'score': round(o['score'], 1), 'signal': round(o['signal'], 6)} for o in assessments],
            'origin_count': len(assessments), 'report_count': sum(len(o['observations']) for o in origins.values()),
            'meaning': 'Editorial judgment of retrieved task reports, not a benchmark measurement or a global model rating.'}


def community_report(data, today):
    models = []
    sources = {s['id']: s for s in data['sources']['sources']}
    source_ids = set()
    research = {r['id']: r for r in data['community_research']['models']}
    for model in data['models']['models']:
        rows = [e for e in data['evidence']['evidence'] if e['model_id'] == model['id']
                and e['kind'] == 'community_test' and evidence_fresh(e, data, today)]
        tasks = sorted({t for e in rows for t in e['direct_tasks'] + e['proxy_tasks']})
        for e in rows:
            source_ids.add(e['source_id'])
            if e['community'].get('applicability'):
                source_ids.add(e['community']['applicability']['source_id'])
        models.append({'model_id': model['id'], 'name': model['name'], 'research': research[model['id']],
                       'tasks': [{'task': t, **community_assessment(rows, t, today)} for t in tasks], 'reports': rows})
    return {'as_of': str(today), 'models': models, 'sources': {sid: sources[sid] for sid in sorted(source_ids)}}


def ranking_support(candidate, candidates, job, data, today):
    """Task-specific editorial support, not estimated intelligence or success probability."""
    policy = data["policy"]["ranking"]
    details = []
    for task in job["tasks"]:
        rows = candidate["evidence"]
        strengths = []
        measured = []
        for ev in rows:
            if ev["kind"] == "community_test":
                continue
            match = 1 if task in ev["direct_tasks"] else 0.45 if task in ev["proxy_tasks"] else 0
            strength = {"independent_eval": 1, "vendor_eval": 0.8, "official_capability": 0.4}[ev["kind"]]
            if not ev["measurement"] and ev["kind"] != "official_capability":
                strength = 0.4
            strengths.append(match * strength)
            if match and ev["measurement"]:
                measured.append(ev)
        # Compare only curated identical protocols, with one observation per group/peer.
        comparisons = {}
        for other in candidates:
            if other is candidate:
                continue
            other_rows = [e for e in other["evidence"] if task in e["direct_tasks"] + e["proxy_tasks"] and e["kind"] != "community_test"]
            for a, b in comparable_pairs(measured, other_rows):
                av, bv = a["measurement"]["value"], b["measurement"]["value"]
                match = 1 if task in a["direct_tasks"] and task in b["direct_tasks"] else 0.45
                comparisons[(a["comparison_group"], other["model_id"])] = (1 if av > bv else 0.5 if av == bv else 0, match)
        peer_wins = sum(v[0] for v in comparisons.values()) / len(comparisons) if comparisons else None
        comparison_support = sum(win*match for win, match in comparisons.values()) / len(comparisons) if comparisons else 0
        strength = max(strengths, default=0)
        # Missing comparisons add no observed support; they are not zero ability.
        formal = 0.75 * strength + 0.25 * comparison_support
        assessment = community_assessment(rows, task, today)
        community = assessment['signal']
        weight = job.get("community_weight", policy["task_community_weights"].get(task, policy["default_community_weight"]))
        details.append({"task": task, "formal_support": round(formal, 6), "evidence_strength": strength,
                        "comparable_peer_win_fraction": peer_wins, "community_signal": round(community, 6),
                        "community_weight": weight, "community_origins": assessment['origin_count'],
                        "community_score": assessment['score'], "community_confidence": assessment['confidence'],
                        "community_mapping": assessment['mapping'],
                        "origins": assessment['origins'],
                        "support": (1-weight)*formal + weight*community})
    return {"support": round(sum(t["support"] for t in details)/len(details), 6), "tasks": details,
            "meaning": "Editorial recommendation support for this task and candidate set; not a probability or global ability score."}


def route(job, data, today=None):
    today = today or date.today()
    validate(data)
    validate_job(job, data)
    job = dict(job)
    language = resolve_language(job.get('language'), job.get('prompt'))
    def say(template, **values):
        return message(template, language, **values)
    if "input_modalities" not in job:
        defaults = {"vision.video": "video", "audio.understand": "audio", "vision.chart": "image",
                    "vision.document": "image", "vision.spatial": "image"}
        job["input_modalities"] = sorted({"text"} | {defaults[t] for t in job["tasks"] if t in defaults})
    tasks = set(job["tasks"])
    sources = {s["id"]: s for s in data["sources"]["sources"]}
    excluded, candidates, relevant = [], [], []
    for ev in data["evidence"]["evidence"]:
        if tasks & set(ev["direct_tasks"] + ev["proxy_tasks"]):
            relevant.append(ev)
    for model in data["models"]["models"]:
        reasons = eligibility(model, job, data, today)
        if reasons:
            excluded.append({"model_id": model["id"], "reasons": reasons})
            continue
        rows = [ev for ev in relevant if ev["model_id"] == model["id"] and evidence_fresh(ev, data, today)]
        weights = data['policy']['ranking']
        coverage = {t for e in rows for t in tasks & set(e['direct_tasks'] + e['proxy_tasks'])
                    if e['kind'] != 'community_test' or (e['community']['rating']['value'] > 5
                    and job.get('community_weight', weights['task_community_weights'].get(t, weights['default_community_weight'])) > 0)}
        if not coverage:
            excluded.append({"model_id": model["id"], "reasons": ["no_fresh_task_evidence"]})
            continue
        direct = set().union(*(set(e["direct_tasks"]) for e in rows if e["measurement"] and e["kind"] != "community_test")) & tasks
        independent = set().union(*(set(e["direct_tasks"]) for e in rows if e["kind"] == "independent_eval")) & tasks
        candidates.append({"model_id": model["id"], "name": model["name"], "direct_tasks": sorted(direct),
                           "independent_tasks": sorted(independent), "covered_tasks": sorted(coverage),
                           "missing_tasks": sorted(tasks - coverage), "evidence": rows,
                           "price": model["price_usd_per_million"], "limitations": catalog_text(data, 'models', model['id'], 'notes', model['notes'], language),
                           "resources": {"access": "user_listed" if "available_models" in job else "verify_account_access",
                                         "input_modalities": model["input_modalities"], "context_tokens": model["context_tokens"],
                                         "tool_calling": model["tool_calling"], "open_weights": model["open_weights"],
                                         "price_applies": bool(model["price_usd_per_million"] and job.get("context_tokens", 0) <= model["price_usd_per_million"]["max_input_tokens"])},
                           "metadata_url": sources[model["source_id"]]["url"]})
    # This is evidence coverage, not a synthetic model intelligence score.
    def key(c):
        return (len(c["covered_tasks"]) == len(tasks), len(c["direct_tasks"]), len(c["independent_tasks"]), len(c["covered_tasks"]))
    for candidate in candidates:
        candidate["ranking"] = ranking_support(candidate, candidates, job, data, today)
    candidates.sort(key=lambda c: (-len(c["covered_tasks"]), -c["ranking"]["support"], c["model_id"]))
    best_coverage = max((key(c) for c in candidates), default=None)
    top = [c for c in candidates if key(c) == best_coverage]
    warnings = []
    if len(candidates) < 3:
        warnings.append(say('Only {count} eligible evidence-backed candidates; missing Top 3 slots are not invented.', count=len(candidates)))
    if any(c["missing_tasks"] for c in candidates[:3]):
        warnings.append(say("Some recommendations cover only part of the request; see missing_tasks or split the work."))
    if job.get("classification_method") == "lexical_fallback":
        warnings.append(say("Lexical classification is provisional; use host semantic classification for ordinary prompts."))
    if job.get("priority") == "latency":
        warnings.append(say("No comparable deployment latency data is bundled; measure end-to-end latency before choosing."))
    primary, decision = None, "insufficient_evidence"
    rationale = say("No eligible candidate has fresh evidence for these tasks. Research the missing evidence.")
    # Pick a measured Pareto-dominant candidate only inside a curated comparable cohort.
    if candidates:
        decision = "shortlist"
        rationale = say("Several candidates or setups remain incomparable; use the task-specific trial below.")
        if len(top) == 1:
            primary = top[0]["model_id"]
            decision = "provisional"
            rationale = say("Best evidence coverage in this catalog; this is not proof of superiority over other models.")
        else:
            for candidate in top:
                wins = []
                for other in top:
                    if other is candidate:
                        continue
                    a = [e for e in candidate["evidence"] if tasks <= set(e["direct_tasks"]) and e["kind"] != "community_test"]
                    b = [e for e in other["evidence"] if tasks <= set(e["direct_tasks"]) and e["kind"] != "community_test"]
                    pairs = comparable_pairs(a, b)
                    wins.append(bool(pairs) and all(ea["measurement"]["value"] > eb["measurement"]["value"]
                                                  for ea, eb in pairs))
                if wins and all(wins):
                    primary = candidate["model_id"]
                    decision = "provisional"
                    rationale = say("Higher observed result within the same recorded comparison cohort; uncertainty and task transfer remain.")
                    break
        if job.get("priority") == "cost":
            priced = [c for c in top if c["price"] and job.get("context_tokens", 0) <= c["price"]["max_input_tokens"]]
            # No assumed input:output ratio: choose only if both prices dominate all peers.
            cheap = [c for c in priced if len(priced) == len(top) and all(
                c["price"]["input"] <= x["price"]["input"] and c["price"]["output"] <= x["price"]["output"]
                for x in priced)]
            if len(cheap) == 1:
                primary = cheap[0]["model_id"]
                decision = "provisional"
                rationale = say("Lowest recorded input and output unit rates among equally covered candidates; total task cost remains unknown.")
            else:
                warnings.append(say("Cost preference cannot be resolved: rates are missing, tied, or have different tradeoffs."))
    current = job.get("current_model")
    switch = {"action": "unknown", "reason": say("Current model was not provided; do not infer it from the assistant's identity.")}
    if current:
        known = {m["id"] for m in data["models"]["models"]}
        eligible_current = next((c for c in candidates if c["model_id"] == current), None)
        hard = next((e["reasons"] for e in excluded if e["model_id"] == current), [])
        hard_incompatible = {"input_modality_not_verified", "context_too_small_or_unknown", "tools_not_verified",
                             "closed_weights", "input_price_over_budget", "output_price_over_budget", "unavailable_or_preview"}
        if current not in known:
            switch = {"action": "unknown", "reason": say("Current model is outside the catalog; verify its exact version and capabilities.")}
        elif candidates and set(hard) & hard_incompatible:
            switch = {"action": "consider_switch", "reason": say('Current model does not meet a verified hard constraint: {constraints}', constraints=', '.join(say(h) for h in hard))}
        elif eligible_current and (primary == current or tasks == {"general.everyday"}):
            switch = {"action": "stay", "reason": say("No demonstrated benefit outweighs moving this task and its context.")}
        elif candidates and eligible_current:
            switch = {"action": "test_first", "reason": say("No matched task trial establishes a worthwhile improvement over the current model.")}
        else:
            switch = {"action": "unknown", "reason": say("Fresh comparable evidence about the current model is missing.")}
    task_map = {t["id"]: t for t in data["taxonomy"]["tasks"]}
    def task_text(task_id, field):
        return catalog_text(data, 'tasks', task_id, field, task_map[task_id][field], language)
    stale = [e["id"] for e in relevant if not evidence_fresh(e, data, today)]
    if stale:
        warnings.append(say('{count} relevant evidence records are stale or future-dated and were excluded.', count=len(stale)))
    if primary and job.get("priority") == "cost":
        candidates.sort(key=lambda c: c["model_id"] != primary)
    elif primary and candidates[0]["model_id"] != primary:
        primary = None
        decision = "shortlist"
        rationale = say("Weighted task support and the comparison cohort differ; choose from Top 3 using access and a task trial.")
    # Display-only prices are attached after every eligibility, ordering, cost
    # preference and switching decision. Selection uses the existing price field.
    models_by_id = {m['id']: m for m in data['models']['models']}
    for candidate in candidates:
        candidate['price_reference'] = price_reference(models_by_id[candidate['model_id']], sources,
                                                       data['policy'], today, language, job.get('context_tokens'))
    recommendations = []
    for rank, c in enumerate(candidates[:3], 1):
        community = any(t["community_origins"] for t in c["ranking"]["tasks"])
        # Name only the tasks backed by each evidence level. A direct result
        # for one task must not make another task's proxy evidence look direct.
        independent_tasks = set(c['independent_tasks'])
        vendor_tasks = set(c['direct_tasks']) - independent_tasks
        remaining_tasks = set(c['covered_tasks']) - independent_tasks - vendor_tasks
        community_only_tasks = {t for t in remaining_tasks if all(
            e['kind'] == 'community_test' for e in c['evidence']
            if t in e['direct_tasks'] + e['proxy_tasks'])}
        groups = [('Task-matched independent evaluation', independent_tasks),
                  ('Task-matched vendor evaluation', vendor_tasks),
                  ('Capability or adjacent-task support', remaining_tasks - community_only_tasks),
                  ('Community task reports only; a task trial is needed', community_only_tasks)]
        reason = ('；' if language == 'zh-CN' else '; ').join(
            say(label) + say(' for ') + ', '.join(task_text(t, 'label') for t in sorted(group))
            for label, group in groups if group)
        if community:
            reason += say("; weighted community reports included (see signed signal and sources)")
        if c["missing_tasks"]:
            reason += say("; partial task coverage")
        recommendations.append({**c, "rank": rank, "reason": reason})
    return {"as_of": today.isoformat(), "snapshot_date": data["models"]["snapshot_date"], 'language': language,
            "classification": [{'id': t, **{k: task_text(t, k) for k in ('domain', 'subdomain', 'label')}} for t in job["tasks"]],
            "classification_method": job.get("classification_method", "structured_job"),
            "decision": decision, "primary": primary, "rationale": rationale,
            "confidence": "insufficient" if not candidates else "limited",
            "recommendations": recommendations, "candidates": candidates, "switch": switch, "excluded": excluded,
            "stale_evidence": stale, "warnings": warnings,
            "validation": [task_text(t, 'validation') for t in job["tasks"]],
            "sources": {sid: sources[sid] for c in candidates for e in c['evidence']
                        for sid in [e['source_id'], *([e['community']['applicability']['source_id']]
                        if e.get('community', {}).get('applicability') else [])]}}


def markdown(result, data=None):
    language = result.get('language', 'en')
    if language == 'zh-CN' and data is None:
        data = load_data()
    def say(template, **values):
        return message(template, language, **values)
    def evidence_text(ev, field, original=None):
        return catalog_text(data, 'evidence', ev['id'], field,
                            ev[field] if original is None else original, language) if data else (ev[field] if original is None else original)
    lines = ["# PromptHarbor", "", " → ".join(t["label"] for t in result["classification"]), "",
             f"**{say('Decision')}:** {say(result['decision'])} · **{say('Confidence')}:** {say(result['confidence'])}",
             '**Top 3:** '+say('choose using task fit and the models you can access.'), '',
             f"**{say('Switch')}:** {say(result['switch']['action'])} — {result['switch']['reason']}", ""]
    lines += shortlist_table(result['recommendations'], language) + ['', price_notice(language), '']
    for candidate in result["recommendations"]:
        lines += [f"## {candidate['rank']}. {candidate['name']}", "", candidate["reason"], ""]
        resources = candidate["resources"]
        lines += [say('Access: {access}; open weights: {weights}; context: {context} tokens.',
                      access=say(resources['access']), weights=say('yes' if resources['open_weights'] else 'no'),
                      context=resources['context_tokens'] or say('unknown'))]
        reference = candidate.get('price_reference')
        lines += ([say('Price reference')+': '+price_cell(reference, language)] if reference
                  else [say('Applicable API price: unknown; check provider and account.')])
        for task in candidate["ranking"]["tasks"]:
            score = f"{task['community_score']}/10" if task['community_score'] is not None else say('not rated')
            lines.append(say('Community: {task}, {score} ({confidence} confidence; {mapping} mapping), weight {weight}, origins {origins}.',
                             task=task['task'], score=score, confidence=say(task['community_confidence']),
                             mapping=say(task['community_mapping']), weight=f"{task['community_weight']:.0%}", origins=task['community_origins']))
        # Keep community evidence visible even when several formal records precede it.
        formal = [e for e in candidate["evidence"] if e["kind"] != "community_test"]
        community = [e for e in candidate["evidence"] if e["kind"] == "community_test"]
        for ev in formal[:2] + community:
            source = result["sources"][ev["source_id"]]
            lines.append(f"- {evidence_text(ev, 'claim')} ({say(ev['kind'])}; {evidence_text(ev, 'setting')}). [{say('Source')}]({source['url']})")
            lines.append(f"  {say('Limit')}: {evidence_text(ev, 'limitations')} {say('Report date')}: {ev['reported_on'] or say('not reported')}; {say('reviewed')} {ev['reviewed_on']}.")
            if ev['kind'] == 'community_test':
                rating = ev['community']['rating']
                lines.append('  '+say('Editorial assessment: {score}/10 — {reason}', score=rating['value'], reason=evidence_text(ev, 'rating_rationale', rating['rationale'])))
                if ev['community'].get('applicability'):
                    a = ev['community']['applicability']
                    source = result['sources'][a['source_id']]
                    lines.append('  '+say('Current-revision relevance: {weight} × — {reason}', weight=a['weight'], reason=evidence_text(ev, 'applicability_reason', a['reason']))+f" [{source['title']}]({source['url']}).")
        lines += ["", say('Limits')+': '+" ".join(candidate["limitations"]), ""]
    lines += ["## "+say('Validation'), ""] + [f"- {v}" for v in result["validation"]]
    if result["warnings"]:
        lines += ["", "## "+say('Selection notes'), ""] + [f"- {v}" for v in result["warnings"]]
    lines += ["", say('As of {as_of}; bundled snapshot {snapshot}.', as_of=result['as_of'], snapshot=result['snapshot_date']), ""]
    return "\n".join(lines)


def audit(data, today):
    due_models = [m["id"] for m in data["models"]["models"] if eligibility(m, {"tasks": []}, data, today) == ["metadata_needs_refresh"]]
    stale = [e["id"] for e in data["evidence"]["evidence"] if not evidence_fresh(e, data, today)]
    research_due = [r['id'] for r in data['community_research']['models']
                    if not 0 <= age_in_days(r['searched_on'], today) <= data['policy']['community_review_days']]
    due_prices = [m['id'] for m in data['models']['models'] if price_refresh_due(m, data['policy'], today)]
    return {"as_of": str(today), "models_needing_refresh": due_models, "stale_evidence": stale,
            "community_searches_due": research_due, 'prices_needing_refresh': due_prices,
            "due": bool(due_models or stale or research_due or due_prices)}


def main(argv=None):
    parser = argparse.ArgumentParser(description="PromptHarbor: task-specific evidence, not an overall model leaderboard.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("taxonomy")
    p = sub.add_parser('community')
    p.add_argument('--as-of', type=iso, default=date.today())
    p = sub.add_parser("classify")
    p.add_argument("prompt", nargs="?")
    p.add_argument("--stdin", action="store_true")
    p = sub.add_parser("recommend")
    choice = p.add_mutually_exclusive_group(required=True)
    choice.add_argument("--job", type=Path)
    choice.add_argument("--prompt")
    choice.add_argument("--stdin", action="store_true")
    p.add_argument("--as-of", type=iso, default=date.today())
    p.add_argument("--format", choices=["json", "markdown"], default="markdown")
    p.add_argument('--language', choices=['auto', 'zh-CN', 'zh', 'en'], help='Override the job language; auto follows the prompt.')
    p = sub.add_parser("audit")
    p.add_argument("--as-of", type=iso, default=date.today())
    p.add_argument("--fail-due", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = load_data()
        validate(data)
        if args.command == "validate":
            output = {"valid": True, "models": len(data["models"]["models"]), "tasks": len(data["taxonomy"]["tasks"]), "evidence": len(data["evidence"]["evidence"])}
        elif args.command == "taxonomy":
            output = data["taxonomy"]
        elif args.command == "classify":
            output = classify(sys.stdin.read() if args.stdin else args.prompt, data)
        elif args.command == "audit":
            output = audit(data, args.as_of)
        elif args.command == 'community':
            output = community_report(data, args.as_of)
        else:
            job = read_json(args.job) if args.job else classify(sys.stdin.read() if args.stdin else args.prompt, data)
            if args.language is not None:
                job['language'] = args.language
            output = route(job, data, args.as_of)
            if args.format == "markdown":
                print(markdown(output))
                return 0
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 1 if args.command == "audit" and args.fail_due and output["due"] else 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"promptharbor: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
