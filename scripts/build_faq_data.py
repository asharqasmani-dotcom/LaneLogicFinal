#!/usr/bin/env python3
"""Generate faq-data.js from the master FAQ prompt file."""

import json
import re
from pathlib import Path

PROMPT = Path("/Users/bstar/Downloads/Lane_Logic_FAQ_Master_Cursor_Prompt.txt")
OUT = Path(__file__).resolve().parent.parent / "faq-data.js"

CATEGORIES = [
    {
        "id": "academy",
        "title": "LANE LOGIC ACADEMY FAQ",
        "description": (
            "Everything you need to know about our world-class training programs, certifications, "
            "courses, and how we help dealers become elite buyers."
        ),
        "icon": "assets/faq/faq-academy.png",
        "iconAlt": "Lane Logic Academy FAQ",
        "marker": "LANE LOGIC ACADEMY FAQ — 20 QUESTIONS AND ANSWERS",
    },
    {
        "id": "listings",
        "title": "LANE LOGIC LISTINGS FAQ",
        "description": (
            "Learn how our private marketplace connects dealers with hand-selected, "
            "high-quality vehicles for maximum profit."
        ),
        "icon": "assets/faq/faq-listings.png",
        "iconAlt": "Lane Logic Listings FAQ",
        "marker": "LANE LOGIC LISTINGS FAQ — 20 QUESTIONS AND ANSWERS",
    },
    {
        "id": "sourcing",
        "title": "LANE LOGIC SOURCING FAQ",
        "description": (
            "Get answers about our full-service vehicle sourcing, our process, "
            "pricing, and how we help dealers buy more and drive more profit."
        ),
        "icon": "assets/faq/faq-sourcing.png",
        "iconAlt": "Lane Logic Sourcing FAQ",
        "marker": "LANE LOGIC SOURCING FAQ — 20 QUESTIONS AND ANSWERS",
    },
]


def extract_section(text: str, marker: str, next_marker=None) -> str:
    start = text.index(marker) + len(marker)
    end = text.index(next_marker) if next_marker else len(text)
    return text[start:end].strip()


def parse_items(section: str) -> list[dict]:
    pattern = re.compile(
        r"(\d+)\.\s*QUESTION:\s*\n(.*?)\n\s*ANSWER:\s*\n(.*?)(?=\n\d+\.\s*QUESTION:|\Z)",
        re.DOTALL,
    )
    items = []
    for match in pattern.finditer(section):
        num = int(match.group(1))
        question = re.sub(r"\s+\n", " ", match.group(2).strip())
        answer = match.group(3).strip()
        answer = re.sub(r"\n{3,}", "\n\n", answer)
        items.append({"number": num, "question": question, "answer": answer})
    items.sort(key=lambda x: x["number"])
    return items


def main() -> None:
    text = PROMPT.read_text(encoding="utf-8")
    data = []
    for i, cat in enumerate(CATEGORIES):
        next_marker = CATEGORIES[i + 1]["marker"] if i + 1 < len(CATEGORIES) else "==================================================\n13. FINAL QA"
        section = extract_section(text, cat["marker"], next_marker)
        items = parse_items(section)
        if len(items) != 20:
            raise SystemExit(f"{cat['id']}: expected 20 items, got {len(items)}")
        data.append({**cat, "items": items})

    js = "window.FAQ_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    OUT.write_text(js, encoding="utf-8")
    print(f"Wrote {OUT} ({sum(len(c['items']) for c in data)} items)")


if __name__ == "__main__":
    main()
