#!/usr/bin/env python3
"""Build the skill's reference files from the TSV data.

    python3 tools/build.py          # writes skills/darijadz/references/{lexicon,verbs}.md and references/examples/*.md
    python3 tools/build.py --check  # only validates the TSVs (used in CI)

data/lexicon/*.tsv   columns: category, darija, variants, arabizi, english, french, msa, note
data/examples/*.tsv  2 columns (darija, english), conversion files (source, darija),
                     16_three_scripts (mixed, arabic, arabizi, english).
Lines starting with "# " are section headings.
"""
import glob
import os
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX = os.path.join(ROOT, "data", "lexicon")
EXS = os.path.join(ROOT, "data", "examples")
REF = os.path.join(ROOT, "skills", "darijadz", "references")
COLS = ["category", "darija", "variants", "arabizi", "english", "french", "msa", "note"]

LEX_TITLES = OrderedDict([
    ("pronoun", "Pronouns"), ("to-be", "To be: راني / راك …"), ("possessive", "Possessives: تاع"),
    ("question", "Question words"), ("demonstrative", "This / that"), ("place", "Place words"),
    ("time", "Time words"), ("connector", "Connectors and fillers"), ("answer", "Yes, no, OK"),
    ("negation", "Negation"), ("quantity", "Quantities"), ("people", "People and family"),
    ("home", "Home"), ("food", "Food and drink"), ("body", "Body and health"), ("places", "Places in town"),
    ("transport", "Transport"), ("money", "Money"), ("adjective", "Adjectives"), ("colour", "Colours"),
    ("thing", "Things"), ("weather", "Weather"), ("ecommerce", "E-commerce"), ("education", "School and university"),
    ("tech", "Tech and social media"), ("feeling", "Feelings"), ("compliment", "Compliments"), ("slang", "Slang"),
    ("culture", "Culture and identity"), ("religion", "Religious and social formulas"), ("social", "Greetings and politeness"),
    ("number", "Numbers"),
])

EX_TITLES = {
    "01_daily": ("daily-life", "Daily life"),
    "02_ecommerce_dm": ("ecommerce-dm", "E-commerce: DMs between customers and sellers"),
    "02b_ecommerce_flows": ("ecommerce-flows", "E-commerce: product-specific flows, confirmation calls, returns, suppliers"),
    "03_ecommerce_ads": ("ecommerce-ads", "E-commerce: ads, product posts, captions and CTAs"),
    "04_customer_service": ("customer-service", "Customer service"),
    "05_content_creators": ("content-creators", "Content creators: hooks, scripts, CTAs, lives"),
    "06_school_middle": ("school-middle", "Middle school (CEM / BEM)"),
    "07_school_secondary": ("school-secondary", "Secondary school (lycée / BAC)"),
    "08_university": ("university", "University"),
    "09_business_freelance": ("business", "Business, freelance and agency"),
    "10_tech_ai": ("tech-ai", "Tech and AI"),
    "11_social_feelings": ("social-feelings", "Feelings and social life"),
    "12_religion_culture": ("religion-culture", "Religion, occasions and culture"),
    "13_services_admin": ("services-admin", "Services, admin, health and transport"),
    "14_msa_to_darija": ("msa-to-darija", "MSA (فصحى) → Darija"),
    "15_fr_en_to_darija": ("fr-en-to-darija", "French / English → Darija"),
    "16_three_scripts": ("three-scripts", "One sentence in three scripts: mixed, Arabic letters, Arabizi"),
    "17_grammar_patterns": ("grammar-patterns", "Grammar in sentences"),
    "18_expressions_proverbs": ("expressions-proverbs", "Proverbs, idioms and formulas"),
    "19_dialogues": ("dialogues", "Short dialogues"),
}
NCOLS = {"16_three_scripts": 4}


def read_tsv(path, ncols):
    rows, errors = [], []
    section = ""
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        if line.startswith("# "):
            section = line[2:].strip()
            rows.append(("H", section))
            continue
        parts = line.split("\t")
        if len(parts) != ncols:
            errors.append(f"{os.path.basename(path)}:{i}: expected {ncols} columns, got {len(parts)}")
            continue
        if not all(p.strip() for p in parts[:2]):
            errors.append(f"{os.path.basename(path)}:{i}: empty field")
        rows.append(("R", parts))
    return rows, errors


def load_lexicon():
    entries, errors = [], []
    for p in sorted(glob.glob(os.path.join(LEX, "*.tsv"))):
        lines = open(p, encoding="utf-8").read().split("\n")
        if lines[0].split("\t") != COLS:
            errors.append(f"{os.path.basename(p)}: bad header")
        for i, l in enumerate(lines[1:], 2):
            if not l.strip():
                continue
            parts = l.split("\t")
            if len(parts) != 8:
                errors.append(f"{os.path.basename(p)}:{i}: expected 8 columns, got {len(parts)}")
                continue
            entries.append(dict(zip(COLS, parts)))
    return entries, errors


def fmt_entry(e):
    s = f"- **{e['darija']}**"
    if e["arabizi"] not in ("", "—"):
        s += f" ({e['arabizi']})"
    s += f" — {e['english']}"
    extra = []
    if e["variants"] not in ("", "—"):
        extra.append(f"also: {e['variants']}")
    if e["french"] not in ("", "—"):
        extra.append(f"FR: {e['french']}")
    if e["msa"] not in ("", "—"):
        extra.append(f"فصحى: {e['msa']}")
    if extra:
        s += " · " + " · ".join(extra)
    if e["note"] not in ("", "—"):
        s += f" · _{e['note']}_"
    return s


def build_lexicon(entries):
    verbs = [e for e in entries if e["category"] == "verb"]
    rest = [e for e in entries if e["category"] != "verb"]
    groups = OrderedDict()
    for e in rest:
        groups.setdefault(e["category"], []).append(e)
    order = [c for c in LEX_TITLES if c in groups] + [c for c in groups if c not in LEX_TITLES]
    out = ["# Lexicon: everyday Algerian Darija words", "",
           "<!-- generated by tools/build.py from data/lexicon/*.tsv; edit the TSV files, not this file -->",
           "<!-- lint:off -->", "",
           f"{len(rest)} entries (plus {len(verbs)} verbs in `verbs.md`). Each line: **Darija** (Arabizi) — English · variants · French · فصحى to avoid · note.",
           "Spellings follow the most frequent forms in a 34M-word corpus of Algerian speech (see CREDITS.md).", "",
           "Sections: " + " · ".join(LEX_TITLES.get(c, c) for c in order), ""]
    for c in order:
        out += [f"## {LEX_TITLES.get(c, c.title())}", ""] + [fmt_entry(e) for e in groups[c]] + [""]
    out.append("<!-- lint:on -->")
    open(os.path.join(REF, "lexicon.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")

    vout = ["# Verbs: past / present, with imperatives", "",
            "<!-- generated by tools/build.py from data/lexicon/02_verbs.tsv -->", "<!-- lint:off -->", "",
            f"{len(verbs)} verbs. Format: **past (he did) / present (he does)** (Arabizi) — English · forms · French · فصحى · note.",
            "Conjugate with the prefixes and endings in `grammar.md` (نـ / تـ / يـ … و).", ""]
    vout += [fmt_entry(e) for e in verbs] + ["", "<!-- lint:on -->"]
    open(os.path.join(REF, "verbs.md"), "w", encoding="utf-8").write("\n".join(vout) + "\n")
    return len(rest), len(verbs)


def build_examples():
    os.makedirs(os.path.join(REF, "examples"), exist_ok=True)
    total, errors, index = 0, [], []
    for p in sorted(glob.glob(os.path.join(EXS, "*.tsv"))):
        stem = os.path.basename(p)[:-4]
        slug, title = EX_TITLES.get(stem, (stem, stem))
        rows, errs = read_tsv(p, NCOLS.get(stem, 2))
        errors += errs
        n = sum(1 for t, _ in rows if t == "R")
        total += n
        out = [f"# Examples: {title}", "",
               f"<!-- generated by tools/build.py from data/examples/{stem}.tsv -->", "",
               f"{n} examples."]
        if stem == "14_msa_to_darija":
            out.append("Format: فصحى → **Darija**. Notice the structure changes, not only the words.")
        elif stem == "15_fr_en_to_darija":
            out.append("Format: French or English → **Darija**.")
        elif stem == "16_three_scripts":
            out.append("Format: mixed (default) | Arabic letters only | Arabizi — English.")
        else:
            out.append("Format: Darija — English.")
        out.append("")
        for t, r in rows:
            if t == "H":
                out += ["", f"## {r}", ""]
            elif stem in ("14_msa_to_darija", "15_fr_en_to_darija"):
                out.append(f"- {r[0]} → **{r[1]}**")
            elif stem == "16_three_scripts":
                out.append(f"- {r[0]} | {r[1]} | {r[2]} — {r[3]}")
            else:
                out.append(f"- {r[0]} — {r[1]}")
        open(os.path.join(REF, "examples", f"{slug}.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
        index.append((slug, title, n))
    return total, index, errors


def main():
    entries, lex_err = load_lexicon()
    if "--check" in sys.argv:
        _, _, ex_err = build_examples_check()
        errs = lex_err + ex_err
    else:
        nlex, nverb = build_lexicon(entries)
        total, index, ex_err = build_examples()
        errs = lex_err + ex_err
        print(f"lexicon: {nlex} entries + {nverb} verbs = {nlex + nverb}")
        print(f"examples: {total} in {len(index)} files")
        for slug, title, n in index:
            print(f"  references/examples/{slug}.md  {n:4d}  {title}")
    for e in errs:
        print("ERROR", e)
    sys.exit(1 if errs else 0)


def build_examples_check():
    errors = []
    total = 0
    for p in sorted(glob.glob(os.path.join(EXS, "*.tsv"))):
        stem = os.path.basename(p)[:-4]
        rows, errs = read_tsv(p, NCOLS.get(stem, 2))
        errors += errs
        total += sum(1 for t, _ in rows if t == "R")
    print(f"examples: {total}")
    return total, None, errors


if __name__ == "__main__":
    main()
