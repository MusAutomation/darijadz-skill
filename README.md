# DarijaDZ 🇩🇿: خلّي الـ AI يهضر بالدارجة الجزائرية الصح

**A free, open skill that makes Claude (and any AI) write real Algerian Darija**, the way we really talk and type. It's not فصحى, it's not Moroccan, and it's not Google Translate.

`1,659 examples` · `689 words and verbs` · `20 domains` · `a linter that catches MSA, Moroccan, Tunisian and Egyptian words` · `MIT licence`

<!-- lint:off -->
---

## بالدارجة

كي تطلب من الـ AI يكتبلك بالدارجة، يعطيك الفصحى، ولا يخلطها مع المغربية ("دابا"، "ديال"، "واخا")، ولا يترجم كلمة بكلمة. **DarijaDZ** يعلّمو كيفاش نهضرو حنا بالصح: راني، راح، ما…ش، تاع، دروك، بزاف، السومة، الكوموند، stop desk… كيما نكتبو في الميساجات، في الإشهار، في الفيديوهات وفي القسم.

**لشكون؟**
- **التجار والـ e-commerce**: الردود في الخاص، تأكيد الكوموند بالتيليفون، الإشهار، الكابشن، التوصيل للدار ولا stop desk، الخلاص كي توصلك، تنقيص الروطور.
- **صناع المحتوى**: hooks، سكريبتات تاع ريلز وتيك توك، CTA، الردود على الكومونتيرات، اللايف.
- **الأساتذة**: المتوسطة (البيام)، الثانوية (الباك) والجامعة. يشرح بالدارجة ويخلي المصطلحات بالفصحى في المدرسة وبالفرنسية في الجامعة.
- **البزنس والفريلانس**: ميساجات للكليان، devis، فواتير، LinkedIn.
- **أي واحد** حاب يحوّل نص من الفصحى ولا الفرنسية ولا الإنجليزية للدارجة.

## Before / after (illustrative)

**Prompt:** _A customer writes "prix svp" under my post. The dress is 3900 DA, delivery to Oran is 600 DA, cash on delivery. Reply in Darija._

| ❌ Typical AI answer | ✅ With DarijaDZ |
|---|---|
| مرحباً بك! سعر الفستان هو 3900 دينار، ورسوم التوصيل إلى وهران 600 دينار. الدفع عند الاستلام. هل تريد أن تطلب الآن؟ | وعليكم السلام، مرحبا بيك 🌸 السومة 3900 دج، والتوصيل لوهران 600 دج للدار. الخلاص كي توصلك. ابعثلي الاسم والنيميرو والبلدية ونأكدولك الكوموند ✅ |
| واش بغيتي دابا؟ عندنا برشا ديال الموديلات زوينين | واش حاب دروك؟ عندنا بزاف الموديلات الشابين |

<!-- lint:on -->

---

## Install

### Claude Code: two lines, nothing to download
Paste these into Claude Code (terminal or VS Code):
```
/plugin marketplace add MusAutomation/darijadz-skill
/plugin install darijadz@musautomation
```
Then just ask: `اكتبلي ردّ بالدارجة لكليان سقسى على السومة`.

### Claude app (web, desktop, mobile: Pro, Max, Team, Enterprise)
1. Download the skill in one click: **[darijadz-skill.zip](https://github.com/MusAutomation/darijadz-skill/raw/main/dist/darijadz-skill.zip)**
2. In Claude, go to **Customize → Skills → + Add → Upload skill** and choose the zip. (Code execution must be on in Settings → Capabilities.)
3. Switch the skill on, then start a new chat.

### ChatGPT, Gemini, Mistral or any other AI
Copy [`prompts/universal-prompt.md`](prompts/universal-prompt.md) into the custom instructions or system prompt.

---

## What's inside
```
skills/darijadz/
  SKILL.md                       the core rules Claude reads first: register, script, grammar, traps, self-check
  references/
    grammar.md                   pronouns, راني and its negatives, conjugation tables, negation, questions, if, comparatives
    verbs.md                     166 verbs: past / present / imperative
    lexicon.md                   523 everyday words: Arabizi, French, the فصحى to avoid, notes
    writing-system.md            mixed vs Arabic-only vs Arabizi; which loanwords go in Arabic letters; corpus-backed spellings
    code-switching.md            how French and English fit inside Darija
    registers.md                 the same message in five registers
    numbers-money-time.md        dinars, centimes, مليون = 10,000 DA, time, days, months (جانفي… ديسمبر)
    regions.md                   west, centre, east, south, Kabylie: what changes
    pitfalls.md                  the 12 ways AI Darija sounds fake, plus an MSA → Darija swap table
    domains/                     playbooks: ecommerce · content-creators · education · business
    examples/                    1,659 real Darija sentences with English, in 20 files
  scripts/darija_lint.py         flags MSA, Moroccan, Tunisian and Egyptian words and suggests the Algerian one
  evals/                         20 test prompts plus a scoring rubric
data/                            the source of truth: lexicon/*.tsv and examples/*.tsv
prompts/universal-prompt.md      for non-Claude AIs
tools/build.py                   rebuilds the references from data/
```

### The 20 example sets
Daily life · e-commerce DMs · e-commerce flows (confirmation calls, returns, suppliers) · ads and captions · customer service · content creators · middle school · lycée and BAC · university · business and freelance · tech and AI · feelings · religion and occasions · services and admin · فصحى → Darija · French and English → Darija · three scripts · grammar in sentences · proverbs and idioms · dialogues.

## Grounded in real speech
Spellings and word choices were checked against **word frequencies from a 34-million-word corpus of Algerian Darija speech** (CC BY 4.0), so the skill prefers `الهضرة` over `الهدرة`, `كاع` over `ڨاع`, `السمانة` over `السيمانة` and `مانيش` over `رانيش`. These are the forms people actually use. All 1,659 examples were written by hand and then linted for MSA and neighbour-dialect leaks. See [CREDITS.md](CREDITS.md).

## Use the linter
```bash
python3 skills/darijadz/scripts/darija_lint.py my_caption.txt
echo "واش بغيتي دابا؟" | python3 skills/darijadz/scripts/darija_lint.py
```
```
<stdin>:1  MEDIUM Moroccan  «بغيتي» → حبيت / نحب / حاب (نبغي is western Algerian)    | واش بغيتي دابا؟
<stdin>:1  HIGH   Moroccan  «دابا» → دروك    | واش بغيتي دابا؟
```

## Contribute 🤝
Darija changes from city to city, and the skill gets better with every native speaker. Add a word to `data/lexicon/*.tsv` or a sentence to `data/examples/*.tsv`, run `python3 tools/build.py`, and open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md). Words from your region (Oran, Constantine, Tizi, the south…) are especially welcome.

---

## Français
**DarijaDZ** est un skill gratuit et open source qui apprend à Claude (et à toute IA) à écrire en vraie darija algérienne : la darija en lettres arabes, le français et l'anglais en lettres latines, avec la grammaire algérienne (راني، راح، ما…ش، تاع). Il contient 1 659 exemples (e-commerce, créateurs de contenu, enseignants du CEM au lycée et à l'université, business), un lexique de 689 mots et verbes, et un linter qui détecte l'arabe standard et les mots marocains, tunisiens ou égyptiens. Installation : voir « Install » ci-dessus. Licence MIT.

## English
**DarijaDZ** is a free, open-source skill that teaches Claude (and any AI) to write genuine Algerian Darija. It includes 1,659 hand-written examples across 20 domains, a 689-entry lexicon checked against a 34M-word speech corpus, domain playbooks for e-commerce, content creation, education and business, a dialect linter and an eval set. MIT licence. Datasets used for validation are credited in [CREDITS.md](CREDITS.md).

---

Made in Algeria 🇩🇿 by **Mus** (@mus_automation). If it helped you, star the repo ⭐ and share it with an Algerian who sells, teaches or creates.
