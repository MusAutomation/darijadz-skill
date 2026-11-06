#!/usr/bin/env python3
"""darija_lint.py: catch words that make Algerian Darija sound like MSA, Moroccan,
Tunisian or Egyptian/Levantine Arabic, and suggest the Algerian word.

Usage:
  python3 darija_lint.py text.txt [more files]     # lint files
  echo "شنو بغيتي دابا" | python3 darija_lint.py   # lint stdin
  python3 darija_lint.py --col 1 examples.tsv       # lint one TSV column (0-based)
  python3 darija_lint.py --strict ...               # exit code 1 if any HIGH finding
  python3 darija_lint.py --json ...                 # machine-readable output

Levels:
  HIGH   almost never said in Algerian Darija; replace it
  MEDIUM said in some regions or registers (check the audience)
  INFO   fine in formal or ad writing, but casual Darija has a more natural word

Lines that contain "lint:ignore" are skipped, and so are blocks between
"lint:off" and "lint:on" (for example in a pitfalls table that lists wrong words on purpose).
Standard library only. MIT licence. Part of the DarijaDZ skill.
"""
import json
import re
import sys

HIGH, MED, INFO = "HIGH", "MEDIUM", "INFO"

# word -> (level, source, Algerian suggestion)
M = {}
def add(level, src, words, sugg):
    for w in words.split():
        M[w] = (level, src, sugg)

# ---------- MSA function words and verbs that casual Darija does not use ----------
add(HIGH, "MSA", "سوف", "راح + verb (راح نبعثلك)")
add(HIGH, "MSA", "لن", "ما … ش (ما نروحش)")
add(HIGH, "MSA", "لقد", "drop it (درت، شفت…)")
add(HIGH, "MSA", "ليس ليست لست لسنا لستم", "ماشي")
add(HIGH, "MSA", "لماذا", "علاش")
add(HIGH, "MSA", "ماذا", "واش")
add(HIGH, "MSA", "متى", "وقتاش")
add(HIGH, "MSA", "أين", "وين")
add(HIGH, "MSA", "هل", "drop it, or start with واش")
add(HIGH, "MSA", "الذي التي الذين اللذين اللتين اللواتي", "اللي")
add(HIGH, "MSA", "يجب ينبغي", "لازم")
add(HIGH, "MSA", "أريد تريد يريد نريد تريدين تريدون", "نحب / حاب / تحب")
add(HIGH, "MSA", "أستطيع تستطيع يستطيع نستطيع تستطيعون", "نقدر / تقدر / يقدر")
add(HIGH, "MSA", "الآن", "دروك")
add(HIGH, "MSA", "جداً جدا", "بزاف")
add(HIGH, "MSA", "أيضاً أيضا", "ثاني / تاني / حتى")
add(HIGH, "MSA", "نعم", "إيه / واه")
add(HIGH, "MSA", "حسناً", "صح / مليح / ok / خلاص")
add(HIGH, "MSA", "ربما", "بالاك / يمكن")
add(HIGH, "MSA", "فقط", "برك / غير")
add(HIGH, "MSA", "عندما", "كي")
add(HIGH, "MSA", "لأن لأنه لأنها لأنني لأننا", "خاطر / على خاطر / لخاطر")
add(HIGH, "MSA", "هؤلاء", "هذو / هادو")
add(HIGH, "MSA", "نحن", "حنا")
add(HIGH, "MSA", "أنتم", "نتوما")
add(HIGH, "MSA", "لدي لديك لديه لديها لدينا لديكم لديهم", "عندي / عندك / عندو…")
add(HIGH, "MSA", "يوجد توجد", "كاين / كاينة")
add(HIGH, "MSA", "منذ", "من / هادي (هادي عامين)")
add(HIGH, "MSA", "دائماً دائما", "ديما")
add(HIGH, "MSA", "قليلاً قليلا", "شوية")
add(HIGH, "MSA", "كثيراً كثيرا", "بزاف")
add(HIGH, "MSA", "انتظر انتظري انتظروا", "استنى / ستنّى / استناو")
add(HIGH, "MSA", "انظر انظري انظروا", "شوف / شوفي / شوفو")
add(HIGH, "MSA", "اذهب اذهبي اذهبوا", "روح / روحي / روحو")
add(HIGH, "MSA", "أعطني أعطيني", "عطيني")
add(HIGH, "MSA", "أخبرني أخبرك", "قولّي / نقولّك")
add(HIGH, "MSA", "أمس", "البارح")
add(HIGH, "MSA", "لذلك لذا", "على هذاك / هذاك علاه")
add(HIGH, "MSA", "سأ", "MSA future: use راح + verb (and سقسى for 'ask')")
add(MED, "MSA", "لكن لكنّ", "بصح")
add(MED, "MSA", "هناك", "كاين / تما / لهيه")
add(MED, "MSA", "هذه", "هادي / هذي")
add(MED, "MSA", "ذلك", "هذاك")
add(MED, "MSA", "تلك", "هذيك")
add(MED, "MSA", "كذلك", "ثاني / تاني")
add(MED, "MSA", "هكذا", "هكا / هكذاك")
add(MED, "MSA", "ذهب ذهبت ذهبنا", "راح / رحت / رحنا")
add(MED, "MSA", "رأيت رأى", "شفت / شاف")
add(MED, "MSA", "اشترى اشتريت", "شرى / شريت")
add(MED, "MSA", "جيد جيدة", "مليح / مليحة")
add(MED, "MSA", "حدث", "صرا")
add(MED, "MSA", "كم", "شحال")
add(INFO, "MSA", "إلى", "لـ (fine in 'من 9 إلى 5')")
add(INFO, "MSA", "جميل جميلة", "شاب / شابة / زين")
add(INFO, "MSA", "الأطفال", "الذراري / الوليدات")
add(INFO, "MSA", "المال", "الدراهم")

# ---------- Moroccan ----------
add(HIGH, "Moroccan", "ديال ديالي ديالك ديالو ديالها ديالنا ديالكم ديالهم", "تاع / تاعي / تاعك / تاعو…")
add(HIGH, "Moroccan", "دابا", "دروك")
add(HIGH, "Moroccan", "واخا", "صح / ok / مليح / خلاص")
add(HIGH, "Moroccan", "عافاك عفاك", "الله يخليك / ربي يخليك")
add(HIGH, "Moroccan", "مكاينش ماكاينش", "ما كانش")
add(HIGH, "Moroccan", "فين", "وين")
add(HIGH, "Moroccan", "فوقاش", "وقتاش")
add(HIGH, "Moroccan", "زوين زوينة زوينين", "شاب / شابة / زين")
add(HIGH, "Moroccan", "هادشي داكشي", "هادي / هذاك / هاد الحاجة")
add(HIGH, "Moroccan", "دغيا", "طول / بالخف / ديراكت")
add(HIGH, "Moroccan", "كنحب كنبغي كندير كنقول كنعرف كنشوف كنمشي كنتمنى كيدير كيقول كيعرف كيبان كتدير كتقول كتعرف", "drop the ك: نحب / ندير / نقول / يدير…")
add(MED, "Moroccan", "مزيان مزيانة", "مليح / مليحة (مزيان is heard in the far west)")
add(MED, "Moroccan", "شنو", "واش (وشنو is western Algerian)")
add(MED, "Moroccan", "آش", "واش")
add(MED, "Moroccan", "بغيت بغيتي نبغي تبغي بغا", "حبيت / نحب / حاب (نبغي is western Algerian)")
add(MED, "Moroccan", "خاصك خاصني خاصنا", "لازم (لازمك / لازمني)")

# ---------- Tunisian ----------
add(HIGH, "Tunisian", "برشا", "بزاف")
add(HIGH, "Tunisian", "فمّا مافماش ماثماش ثمة", "كاين / ما كانش")
add(HIGH, "Tunisian", "يعيشك يعيشكم", "يعطيك الصحة / صحيت")
add(HIGH, "Tunisian", "شبيك شبيكم", "واش بيك")
add(HIGH, "Tunisian", "شنية شنوة", "واش")
add(MED, "Tunisian", "توّا توا", "دروك")
add(MED, "Tunisian", "باهي باهية", "مليح / مليحة / صح")
add(MED, "Tunisian", "ننجم تنجم ينجم نجمت", "نقدر / تقدر / يقدر")
add(MED, "Tunisian", "زادة", "ثاني / تاني")
add(MED, "Tunisian", "يزّي", "بركا / خلاص")

# ---------- Egyptian / Levantine ----------
add(HIGH, "Egyptian", "عايز عاوز عايزة عاوزة", "حاب / نحب")
add(HIGH, "Egyptian", "دلوقتي", "دروك")
add(HIGH, "Egyptian", "كده كدا", "هكا")
add(HIGH, "Egyptian", "مش", "ماشي / ما … ش")
add(HIGH, "Egyptian", "بتاع بتاعي بتاعك بتاعه بتاعها", "تاع / تاعي / تاعك…")
add(HIGH, "Egyptian", "أوي", "بزاف")
add(HIGH, "Egyptian", "ازيك إزيك ازاي إزاي", "واش راك / كيفاش")
add(HIGH, "Egyptian", "امتى إمتى", "وقتاش")
add(HIGH, "Egyptian", "ده", "هذا")
add(HIGH, "Levantine", "هيك", "هكا")
add(HIGH, "Levantine", "هلق هلأ", "دروك")
add(HIGH, "Levantine", "كتير", "بزاف")
add(HIGH, "Levantine", "منيح منيحة", "مليح / مليحة")
add(HIGH, "Egyptian", "بكام", "بشحال")
add(HIGH, "Egyptian", "عشان علشان", "خاطر / باش")
add(HIGH, "Levantine", "هيدا هيدي", "هذا / هادي")
add(HIGH, "Gulf", "شلونك شلونكم", "واش راك / كي راك")
add(HIGH, "Gulf", "وايد", "بزاف")
add(MED, "Levantine", "بدي بدك", "نحب / حاب")
add(MED, "Levantine", "شو", "واش")
add(MED, "Egyptian", "بس", "برك / غير / بصح")
add(MED, "Egyptian", "فلوس الفلوس", "الدراهم")
add(MED, "Egyptian", "ليه", "علاش")

PHRASES = [  # multi-word patterns (checked on the raw line)
    (HIGH, "MSA", "كيف حالك", "واش راك / كي راك"),
    (HIGH, "MSA", "ماذا تريد", "واش حاب"),
    (HIGH, "MSA", "لا يوجد", "ما كانش"),
    (HIGH, "MSA", "لا أعرف", "ما نعرفش"),
    (HIGH, "MSA", "شكراً جزيلاً", "يعطيك الصحة / صحيت بزاف"),
    (MED, "MSA", "من أجل", "باش / على جال"),
    (INFO, "MSA", "من فضلك", "الله يخليك / ربي يخليك"),
]

HARAKAT = re.compile("[\u064B-\u0652\u0670\u0640]")
def norm(w):
    return HARAKAT.sub("", w).replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي")

# matched only exactly as written (their normalised form is a different Darija word)
RAW_ONLY = {"أبداً": (INFO, "MSA", "قاع / والو / حتى نهار"),   # ابدا = 'start!'
            "أمس": (HIGH, "MSA", "البارح")}
M.pop("أمس", None)
NM = {}
for k, v in M.items():
    NM.setdefault(norm(k), v)
SAFE = {"وشنو", "فوايد"}  # normalised words that are fine in Algerian Darija (وشنو = western "what")

TOKEN = re.compile("[\u0621-\u063A\u0640-\u0652\u0670-\u06D3]+")  # Arabic letters + harakat, without ، ؛ ؟
PREFIX = ("و", "ف")      # و/ف glued to the next word

def check_token(raw):
    n = norm(raw)
    hit = None
    if raw in RAW_ONLY:
        return RAW_ONLY[raw]
    if raw in M:
        hit = M[raw]
    elif n in NM and n not in SAFE:
        hit = NM[n]
    elif len(n) > 3 and n[0] in PREFIX and n[1:] in NM and n not in SAFE and n[1:] not in SAFE:
        hit = NM[n[1:]]
    if raw.startswith("سأ") and len(raw) >= 5:  # MSA future prefix: سأرسل، سأكتب
        hit = M["سأ"]
    return hit

def lint_line(line):
    out = []
    for m in TOKEN.finditer(line):
        raw = m.group(0)
        hit = check_token(raw)
        if hit:
            out.append({"word": raw, "level": hit[0], "dialect": hit[1], "use": hit[2], "col": m.start()})
    for level, src, pat, sugg in PHRASES:
        if pat in line:
            out.append({"word": pat, "level": level, "dialect": src, "use": sugg, "col": line.find(pat)})
    return out

def main(argv):
    strict = "--strict" in argv
    as_json = "--json" in argv
    col = None
    files = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--col":
            col = int(argv[i + 1]); i += 2; continue
        if not a.startswith("--"):
            files.append(a)
        i += 1
    sources = [(f, open(f, encoding="utf-8")) for f in files] or [("<stdin>", sys.stdin)]
    findings = []
    for name, fh in sources:
        off = False
        for n, line in enumerate(fh, 1):
            if "lint:off" in line:
                off = True
            if "lint:on" in line:
                off = False
                continue
            if off or "lint:ignore" in line:
                continue
            text = line.rstrip("\n")
            if col is not None:
                parts = text.split("\t")
                if len(parts) <= col:
                    continue
                text = parts[col]
            for f in lint_line(text):
                f.update({"file": name, "line": n, "text": text.strip()[:120]})
                findings.append(f)
    if as_json:
        print(json.dumps(findings, ensure_ascii=False, indent=1))
    else:
        for f in findings:
            print(f"{f['file']}:{f['line']}  {f['level']:<6} {f['dialect']:<9} «{f['word']}» → {f['use']}    | {f['text']}")
        counts = {lv: sum(1 for f in findings if f["level"] == lv) for lv in (HIGH, MED, INFO)}
        print(f"\n{len(findings)} findings  (HIGH {counts[HIGH]}, MEDIUM {counts[MED]}, INFO {counts[INFO]})", file=sys.stderr)
    if strict and any(f["level"] == HIGH for f in findings):
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
