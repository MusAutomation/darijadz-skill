# Testing DarijaDZ

`evals.json` holds 20 prompts across e-commerce, teaching, content, business, Arabizi, money and honesty. Run each prompt **with** and **without** the skill and compare.

## Score each answer (0 to 2 per line, 14 max)

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| **Algerian, not MSA** | reads like news or a textbook | a few MSA words | sounds spoken, with Algerian connectors |
| **No neighbour dialects** | Moroccan, Tunisian or Egyptian words | one slip | none |
| **Grammar** | wrong person or gender, or no ما…ش | small slips | راني / راح / ما…ش / تاع all natural |
| **Register** | wrong for the audience | mostly right | exactly right (school terms in فصحى, uni terms in French, polite customer service) |
| **Script** | inconsistent | mostly consistent | follows the default or mirrors the user |
| **Facts and honesty** | invents prices, reviews or claims | vague | uses the given facts only, with placeholders otherwise |
| **Would an Algerian send it as is?** | no | with edits | yes |

## Automatic check
Save each answer to a file and run:
```
python3 scripts/darija_lint.py answer.txt
```
A good answer has **0 HIGH** findings. MEDIUM findings need a human look, because they may be regional and correct.

## Human check (the real test)
Ask 3 Algerians from different regions to read 5 answers each and tell you which words they would change. Add their fixes to `data/lexicon` or `data/examples` and open a pull request.
