"""Load the content files and walk the text in them.

Citations are written inline as {{passage-id other-id}}. Every id must be an
entry in text/passages.yaml.
"""

import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITE = re.compile(r"\{\{([a-z0-9 -]+)\}\}")
URL = re.compile(r"https?://\S+")


def load():
    data = {}
    for name, key in (("sources", "sources"), ("passages", "evidence"), ("explainer", None), ("summary", None)):
        with open(os.path.join(ROOT, "text", name + ".yaml"), encoding="utf-8") as fh:
            loaded = yaml.safe_load(fh)
        data[key or name] = loaded[name] if key else loaded
    for number, src in enumerate(data["sources"], 1):
        src["n"] = number
    _check_text(data["explainer"], "explainer")
    _check_text(data["summary"], "summary")
    return data


def _check_text(node, path):
    """A list item with ': ' in it is read by YAML as a mapping. Catch that early."""
    if isinstance(node, dict):
        for key, value in node.items():
            _check_text(value, f"{path}.{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            if isinstance(value, dict) and path.rsplit(".", 1)[-1] in ("law", "meaning", "companies", "unsettled", "items", "paragraphs", "thread", "rows"):
                raise ValueError(f"{path}[{i}] was read as a mapping; put the text in quotes")
            _check_text(value, f"{path}[{i}]")


def cite_ids(text):
    ids = []
    for match in CITE.finditer(text):
        ids.extend(match.group(1).split())
    return ids


def _cells(table):
    for row in table.get("rows", []):
        yield " ".join(row)


def walk(data):
    """Yield (where, kind, text) for every piece of prose in the deliverables.

    kind is "law" for text that states the law or reports what a source says
    (it must be cited), and "prose" for everything else.
    """
    ex = data["explainer"]
    yield "notice", "prose", ex["notice"]
    for i, item in enumerate(ex["key_dates"], 1):
        yield f"key date {i}", "law", item["label"]
    for i, item in enumerate(ex["short"], 1):
        yield f"short {i}", "law", item["a"]
    for sec in ex["sections"]:
        sid = sec["id"]
        yield f"{sid} lede", "prose", sec.get("lede", "")
        for i, text in enumerate(sec.get("law", []), 1):
            yield f"{sid} law {i}", "law", text
        if "law_table" in sec:
            for i, row in enumerate(_cells(sec["law_table"]), 1):
                yield f"{sid} table row {i}", "law", row
        for i, item in enumerate(sec.get("timeline", []), 1):
            yield f"{sid} timeline {i}", "law", item["text"]
        for i, text in enumerate(sec.get("companies", []), 1):
            yield f"{sid} companies {i}", "law", text
        if "fit_table" in sec:
            for i, row in enumerate(sec["fit_table"]["rows"], 1):
                yield f"{sid} fit row {i}", "law", " ".join(row[:2])
                yield f"{sid} fit row {i} reading", "prose", row[2]
        for i, text in enumerate(sec.get("meaning", []), 1):
            yield f"{sid} meaning {i}", "prose", text
        if "steps" in sec:
            for i, text in enumerate(sec["steps"]["items"], 1):
                yield f"{sid} step {i}", "law", text
            yield f"{sid} steps note", "prose", sec["steps"].get("note", "")
        if "meaning_table" in sec:
            for i, row in enumerate(_cells(sec["meaning_table"]), 1):
                yield f"{sid} roles row {i}", "law", row
        for i, text in enumerate(sec.get("unsettled", []), 1):
            yield f"{sid} unsettled {i}", "prose", text
        for i, text in enumerate(sec.get("checklist", {}).get("items", []), 1):
            yield f"{sid} checklist {i}", "prose", text
        if "callout" in sec:
            for i, text in enumerate(sec["callout"]["paragraphs"], 1):
                yield f"{sid} callout {i}", "law", text
    sm = data["summary"]
    for i, text in enumerate(sm["paragraphs"], 1):
        yield f"summary {i}", "law", text
    for i, text in enumerate(sm["thread"], 1):
        yield f"thread {i}", "prose", text


def citations(data):
    for where, _, text in walk(data):
        ids = cite_ids(text)
        if ids:
            yield where, ids


def law_paragraphs(data):
    for where, kind, text in walk(data):
        if kind == "law" and text.strip():
            yield where, text


def all_prose(data):
    for where, _, text in walk(data):
        yield where, CITE.sub("", text)


def x_length(post):
    """Length of a post as X counts it: every link counts as 23 characters."""
    return len(URL.sub("x" * 23, post))
