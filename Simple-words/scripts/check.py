#!/usr/bin/env python3
"""
check.py — flag any word that is NOT in the "ten hundred" simple-word list.

This is the simplewriter-style checker for the simple-words skill. Write your
explanation, then run it through this script. Every word it flags is a word you
are NOT allowed to use (unless it is a technical term you have deliberately
introduced and explained — pass those with --allow).

Usage:
    python3 check.py "your text here"
    python3 check.py < file.txt
    echo "your text" | python3 check.py
    python3 check.py --allow "dna,neuron" "your text about dna"

Exit code is 0 if the text is clean, 1 if any word is flagged. The flagged
words are printed one per line as: WORD  (xN)  ->  seen as "original token"
"""
import sys
import os
import re
import json
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
LIST_PATH = os.path.join(HERE, "..", "references", "word_list.txt")
IRREG_PATH = os.path.join(HERE, "irregulars.json")


def load_allowed():
    with open(LIST_PATH, encoding="utf-8") as f:
        words = {line.strip().lower() for line in f if line.strip()}
    return words


ALLOWED = load_allowed()

# Irregular forms (went->go, us->we, children->child, better->good, was->be...).
# These can't be reached by chopping suffixes, so we map them explicitly.
try:
    with open(IRREG_PATH, encoding="utf-8") as f:
        IRREGULAR = {k.lower(): v.lower() for k, v in json.load(f).items()}
except FileNotFoundError:
    IRREGULAR = {}

# Contraction tails: strip these, then check the stem.
TAILS = ["n't", "'re", "'ve", "'ll", "'d", "'m", "'s", "’re", "’ve", "’ll",
         "’d", "’m", "’s", "n’t"]


def candidate_bases(w):
    """Yield possible base forms of an inflected word to test against the list.
    We accept a word if ANY candidate base is in the allowed set. This lets
    talk/talks/talking/talked, big/bigger/biggest, quick/quickly, etc. all pass
    from a single listed base word (matching Munroe's 'word forms count as one').
    """
    yield w
    # possessive / plural / 3rd person -s
    if w.endswith("s") and len(w) > 1:
        yield w[:-1]
    if w.endswith("es") and len(w) > 2:
        yield w[:-2]
    if w.endswith("ies") and len(w) > 3:
        yield w[:-3] + "y"
    # past tense -ed
    if w.endswith("ed") and len(w) > 2:
        yield w[:-2]           # walked -> walk
        yield w[:-1]           # liked -> like
        if len(w) > 3 and w[-3] == w[-4]:
            yield w[:-3]       # stopped -> stop
    if w.endswith("ied") and len(w) > 3:
        yield w[:-3] + "y"     # tried -> try
    # -ing
    if w.endswith("ing") and len(w) > 3:
        yield w[:-3]           # walking -> walk
        yield w[:-3] + "e"     # making -> make
        if len(w) > 4 and w[-4] == w[-5]:
            yield w[:-4]       # running -> run
    # comparative / superlative / agent -er/-est
    if w.endswith("er") and len(w) > 2:
        yield w[:-2]           # teacher -> teach, bigger... 
        yield w[:-1]           # nicer -> nice
        if len(w) > 3 and w[-3] == w[-4]:
            yield w[:-3]       # bigger -> big
    if w.endswith("est") and len(w) > 3:
        yield w[:-3]
        yield w[:-2]
        if len(w) > 4 and w[-4] == w[-5]:
            yield w[:-4]       # biggest -> big
    # adverb -ly
    if w.endswith("ly") and len(w) > 2:
        yield w[:-2]           # quickly -> quick
    if w.endswith("ily") and len(w) > 3:
        yield w[:-3] + "y"     # happily -> happy


def is_allowed(token, extra):
    # strip contraction tails first
    t = token
    for tail in TAILS:
        if t.endswith(tail) and len(t) > len(tail):
            t = t[: -len(tail)]
            break
    t = t.strip("'’")
    if not t:
        return True
    if t in extra or t in ALLOWED:
        return True
    # irregular form of a listed word (went -> go, us -> we, was -> be)
    if IRREGULAR.get(t) in ALLOWED:
        return True
    for base in candidate_bases(t):
        if base in ALLOWED or base in extra:
            return True
    return False


# a "word" is letters, optionally with internal apostrophes (don't, it's)
TOKEN_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")


def check(text, extra):
    flagged = {}  # lower-word -> (count, first_original)
    for m in TOKEN_RE.finditer(text):
        orig = m.group(0)
        low = orig.lower()
        if is_allowed(low, extra):
            continue
        if low not in flagged:
            flagged[low] = [0, orig]
        flagged[low][0] += 1
    return flagged


def main():
    ap = argparse.ArgumentParser(description="Flag words not in the ten-hundred list.")
    ap.add_argument("text", nargs="?", help="text to check (or pipe via stdin)")
    ap.add_argument("--allow", default="",
                    help="comma-separated technical terms to treat as allowed")
    args = ap.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    extra = {w.strip().lower() for w in args.allow.split(",") if w.strip()}

    flagged = check(text, extra)
    if not flagged:
        print("CLEAN — every word is in the ten hundred (or an allowed term).")
        sys.exit(0)

    total = sum(v[0] for v in flagged.values())
    print(f"FLAGGED {len(flagged)} disallowed word(s), {total} time(s) total:\n")
    for low in sorted(flagged, key=lambda k: (-flagged[k][0], k)):
        cnt, orig = flagged[low]
        note = f'  ->  seen as "{orig}"' if orig.lower() != low else ""
        print(f'  {low}  (x{cnt}){note}')
    sys.exit(1)


if __name__ == "__main__":
    main()
