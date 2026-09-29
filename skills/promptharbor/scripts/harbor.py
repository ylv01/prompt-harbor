"""Evidence retrieval and conservative model shortlisting. Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"independent_eval", "vendor_eval", "official_capability", "community_test"}
MODALITIES = {"text", "image", "video", "audio"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def load_data(root=ROOT):
    return {name: read_json(root / "data" / f"{name}.json")
            for name in ("taxonomy", "models", "sources", "evidence", "policy")}


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
    groups = {}
    for ev in data["evidence"]["evidence"]:
        group = ev.get("comparison_group")
        if group:
            m = ev["measurement"]
            key = (ev["source_id"], m["benchmark"], m["version"], m["metric"], m["unit"], m["protocol"])
            require(group not in groups or groups[group] == key, "Incompatible comparison group")
            groups[group] = key
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
               "open_weights_only", "allow_preview", "priority", "max_input_price", "max_output_price", "community_weight"}
    require(isinstance(job, dict) and not set(job) - allowed, "Unknown job field")
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
        origins = {}
        for ev in rows:
            if ev["kind"] != "community_test":
                continue
            match = 1 if task in ev["direct_tasks"] else 0.45 if task in ev["proxy_tasks"] else 0
            if not match:
                continue
            c = ev["community"]
            quality = {"reproduced": 1, "artifact_report": 0.6, "firsthand": 0.2}[c["grade"]]
            freshness = (0.5 ** (age_in_days(ev["reported_on"], today) / 60)
                         if ev["reported_on"] else 0.5)
            signal = {"positive": 1, "negative": -1, "mixed": 0}[c["stance"]] * quality * match * freshness
            # Copies of one report never multiply its effect. Contradictions remain visible.
            origin = origins.setdefault(c["origin_id"], {"signals": set(), "evidence_ids": []})
            origin["signals"].add(signal)
            origin["evidence_ids"].append(ev["id"])
        values = [sum(o["signals"]) / len(o["signals"]) for o in origins.values()]
        community = sum(values) / max(3, len(values))
        weight = job.get("community_weight", policy["task_community_weights"].get(task, policy["default_community_weight"]))
        details.append({"task": task, "formal_support": round(formal, 6), "evidence_strength": strength,
                        "comparable_peer_win_fraction": peer_wins, "community_signal": round(community, 6),
                        "community_weight": weight, "community_origins": len(origins),
                        "origins": [{"origin_id": k, "signal": round(sum(v["signals"])/len(v["signals"]), 6),
                                     "evidence_ids": v["evidence_ids"]} for k, v in sorted(origins.items())],
                        "support": (1-weight)*formal + weight*community})
    return {"support": round(sum(t["support"] for t in details)/len(details), 6), "tasks": details,
            "meaning": "Editorial recommendation support for this task and candidate set; not a probability or global ability score."}


def route(job, data, today=None):
    today = today or date.today()
    validate(data)
    validate_job(job, data)
    job = dict(job)
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
                    if e['kind'] != 'community_test' or (e['community']['stance'] == 'positive'
                    and job.get('community_weight', weights['task_community_weights'].get(t, weights['default_community_weight'])) > 0)}
        if not coverage:
            excluded.append({"model_id": model["id"], "reasons": ["no_fresh_task_evidence"]})
            continue
        direct = set().union(*(set(e["direct_tasks"]) for e in rows if e["measurement"] and e["kind"] != "community_test")) & tasks
        independent = set().union(*(set(e["direct_tasks"]) for e in rows if e["kind"] == "independent_eval")) & tasks
        candidates.append({"model_id": model["id"], "name": model["name"], "direct_tasks": sorted(direct),
                           "independent_tasks": sorted(independent), "covered_tasks": sorted(coverage),
                           "missing_tasks": sorted(tasks - coverage), "evidence": rows,
                           "price": model["price_usd_per_million"], "limitations": model["notes"],
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
        warnings.append(f"Only {len(candidates)} eligible evidence-backed candidates; missing Top 3 slots are not invented.")
    if any(c["missing_tasks"] for c in candidates[:3]):
        warnings.append("Some recommendations cover only part of the request; see missing_tasks or split the work.")
    if job.get("classification_method") == "lexical_fallback":
        warnings.append("Lexical classification is provisional; use host semantic classification for ordinary prompts.")
    if job.get("priority") == "latency":
        warnings.append("No comparable deployment latency data is bundled; measure end-to-end latency before choosing.")
    primary, decision = None, "insufficient_evidence"
    rationale = "No eligible candidate has fresh evidence for these tasks. Research the missing evidence."
    # Pick a measured Pareto-dominant candidate only inside a curated comparable cohort.
    if candidates:
        decision = "shortlist"
        rationale = "Several candidates or setups remain incomparable; use the task-specific trial below."
        if len(top) == 1:
            primary = top[0]["model_id"]
            decision = "provisional"
            rationale = "Best evidence coverage in this catalog; this is not proof of superiority over other models."
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
                    rationale = "Higher observed result within the same recorded comparison cohort; uncertainty and task transfer remain."
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
                rationale = "Lowest recorded input and output unit rates among equally covered candidates; total task cost remains unknown."
            else:
                warnings.append("Cost preference cannot be resolved: rates are missing, tied, or have different tradeoffs.")
    current = job.get("current_model")
    switch = {"action": "unknown", "reason": "Current model was not provided; do not infer it from the assistant's identity."}
    if current:
        known = {m["id"] for m in data["models"]["models"]}
        eligible_current = next((c for c in candidates if c["model_id"] == current), None)
        hard = next((e["reasons"] for e in excluded if e["model_id"] == current), [])
        hard_incompatible = {"input_modality_not_verified", "context_too_small_or_unknown", "tools_not_verified",
                             "closed_weights", "input_price_over_budget", "output_price_over_budget", "unavailable_or_preview"}
        if current not in known:
            switch = {"action": "unknown", "reason": "Current model is outside the catalog; verify its exact version and capabilities."}
        elif candidates and set(hard) & hard_incompatible:
            switch = {"action": "consider_switch", "reason": "Current model does not meet a verified hard constraint: " + ", ".join(hard)}
        elif eligible_current and (primary == current or tasks == {"general.everyday"}):
            switch = {"action": "stay", "reason": "No demonstrated benefit outweighs moving this task and its context."}
        elif candidates and eligible_current:
            switch = {"action": "test_first", "reason": "No matched task trial establishes a worthwhile improvement over the current model."}
        else:
            switch = {"action": "unknown", "reason": "Fresh comparable evidence about the current model is missing."}
    task_map = {t["id"]: t for t in data["taxonomy"]["tasks"]}
    stale = [e["id"] for e in relevant if not evidence_fresh(e, data, today)]
    if stale:
        warnings.append(f"{len(stale)} relevant evidence records are stale or future-dated and were excluded.")
    if primary and job.get("priority") == "cost":
        candidates.sort(key=lambda c: c["model_id"] != primary)
    elif primary and candidates[0]["model_id"] != primary:
        primary = None
        decision = "shortlist"
        rationale = "Weighted task support and the comparison cohort differ; choose from Top 3 using access and a task trial."
    recommendations = []
    for rank, c in enumerate(candidates[:3], 1):
        community = any(t["community_origins"] for t in c["ranking"]["tasks"])
        reason = ("Task-matched independent evaluation" if c["independent_tasks"] else
                  "Task-matched vendor evaluation" if c["direct_tasks"] else "Capability or adjacent-task support")
        if all(e['kind'] == 'community_test' for e in c['evidence']):
            reason = "Community task reports only; a task trial is needed"
        reason += " for " + ", ".join(task_map[t]["label"] for t in c["covered_tasks"])
        if community:
            reason += "; weighted community reports included (see signed signal and sources)"
        if c["missing_tasks"]:
            reason += "; partial task coverage"
        recommendations.append({**c, "rank": rank, "reason": reason})
    return {"as_of": today.isoformat(), "snapshot_date": data["models"]["snapshot_date"],
            "classification": [{k: task_map[t][k] for k in ("id", "domain", "subdomain", "label")} for t in job["tasks"]],
            "classification_method": job.get("classification_method", "structured_job"),
            "decision": decision, "primary": primary, "rationale": rationale,
            "confidence": "insufficient" if not candidates else "limited",
            "recommendations": recommendations, "candidates": candidates, "switch": switch, "excluded": excluded,
            "stale_evidence": stale, "warnings": warnings,
            "validation": [task_map[t]["validation"] for t in job["tasks"]],
            "sources": {e["source_id"]: sources[e["source_id"]] for c in candidates for e in c["evidence"]}}


def markdown(result):
    lines = ["# PromptHarbor", "", " → ".join(t["label"] for t in result["classification"]), "",
             f"**Decision:** {result['decision']} · **Confidence:** {result['confidence']}",
             "**Top 3:** choose using task fit and the models you can access.", "",
             f"**Switch:** {result['switch']['action']} — {result['switch']['reason']}", ""]
    for candidate in result["recommendations"]:
        lines += [f"## {candidate['rank']}. {candidate['name']}", "", candidate["reason"], ""]
        resources = candidate["resources"]
        lines += [f"Access: {resources['access']}; open weights: {resources['open_weights']}; context: {resources['context_tokens'] or 'unknown'} tokens."]
        price = candidate["price"]
        lines += ([f"Recorded API input/output: ${price['input']}/${price['output']} per million tokens; subscription entitlement is separate."]
                  if resources["price_applies"] else ["Applicable API price: unknown; check provider and account."])
        for task in candidate["ranking"]["tasks"]:
            lines.append(f"Community: {task['task']}, weight {task['community_weight']:.0%}, signed signal {task['community_signal']:+.3f}, independent origins {task['community_origins']}.")
        # Keep community evidence visible even when several formal records precede it.
        formal = [e for e in candidate["evidence"] if e["kind"] != "community_test"]
        community = [e for e in candidate["evidence"] if e["kind"] == "community_test"]
        for ev in formal[:2] + community:
            source = result["sources"][ev["source_id"]]
            lines.append(f"- {ev['claim']} ({ev['kind']}; {ev['setting']}). [Source]({source['url']})")
            lines.append(f"  Limit: {ev['limitations']} Report date: {ev['reported_on'] or 'not reported'}; reviewed {ev['reviewed_on']}.")
        lines += ["", "Limits: " + " ".join(candidate["limitations"]), ""]
    lines += ["## Validation", ""] + [f"- {v}" for v in result["validation"]]
    if result["warnings"]:
        lines += ["", "## Selection notes", ""] + [f"- {v}" for v in result["warnings"]]
    lines += ["", f"As of {result['as_of']}; bundled snapshot {result['snapshot_date']}.", ""]
    return "\n".join(lines)


def audit(data, today):
    due_models = [m["id"] for m in data["models"]["models"] if eligibility(m, {"tasks": []}, data, today) == ["metadata_needs_refresh"]]
    stale = [e["id"] for e in data["evidence"]["evidence"] if not evidence_fresh(e, data, today)]
    return {"as_of": str(today), "models_needing_refresh": due_models, "stale_evidence": stale,
            "due": bool(due_models or stale)}


def main(argv=None):
    parser = argparse.ArgumentParser(description="PromptHarbor: task-specific evidence, not an overall model leaderboard.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("taxonomy")
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
        else:
            job = read_json(args.job) if args.job else classify(sys.stdin.read() if args.stdin else args.prompt, data)
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
