# Contributing to DarijaDZ

صحيت على المساهمة! Every native speaker makes the skill better.

## Add a word
Edit the right file in `data/lexicon/`. The files are tab-separated with 8 columns:
```
category	darija	variants	arabizi	english	french	msa	note
ecommerce	السومة	البري، le prix	souma	price	prix	السعر	شحال السومة؟
```
- `darija`: the most common Algerian spelling.
- `variants`: other spellings or regional forms, separated by `،`.
- `msa`: the فصحى word people should **avoid** in casual Darija.
- Use `—` for an empty field.

## Add example sentences
Add lines to a file in `data/examples/`, as Darija TAB English (or source TAB Darija for `14_` and `15_`). Lines starting with `# ` are section headings.
Good examples are:
- something a real Algerian would say or type, as is;
- short (one or two sentences);
- free of brand claims, private names or politics.

## Before opening a pull request
```bash
python3 tools/build.py                  # rebuilds skills/darijadz/references from data/
python3 skills/darijadz/scripts/darija_lint.py --col 0 data/examples/01_daily.tsv
```
Fix any **HIGH** findings, or explain in the PR why the word is right for your region.

## Regional words
Say where you're from in the PR (e.g. "Oran", "Sétif", "Tizi Ouzou"). Regional forms go in `variants` with a note such as `(west)`. The main form stays the one most Algerians understand.

## Code of conduct
Be kind. Darija has no single "correct" form, and every city's Darija is real Darija.
