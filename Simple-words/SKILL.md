---
name: simple-words
description: >-
  Explain anything in English using ONLY the "ten hundred" (≈1000) most common
  simple words — the strict word list from Randall Munroe's "Thing Explainer"
  and the Up-Goer Five. No matter how hard the topic, every word in the answer
  must come from that list (word forms like talk/talking/talked count as one).
  Technical terms are allowed only when introduced and then explained in simple
  words. This is the STRICT, checkable version — it verifies the output with a
  script, unlike loose "explain simply" styles.

  Use this skill whenever the user asks to explain something "using only the
  ten hundred / thousand simple words", "simple words only", "Up-Goer Five
  style", "thing-explainer strict", "no big words", "hard mode simple", or
  types /simplewords. Also use it any time the user makes clear they want the
  answer locked to the simple-word list rather than just "kept easy". Always
  run the checker before answering — never skip it.
---

# Simple Words

Explain any thing in English using **only the ten hundred most common words**.
The topic can be as hard as you like — a black hole, taxes, a computer chip —
but the words used to explain it must all come from the fixed list. This is the
strict, *checkable* version of simple explaining, in the spirit of Randall
Munroe's *Thing Explainer* and his Up-Goer Five (where he explained a giant
space rocket using only these words).

## The one hard rule

Every word in your answer must be one of the ~1000 words in
`references/word_list.txt`, **or** a different form of one of those words.

- **Word forms count as one.** If `talk` is in the list, then `talks`, `talked`,
  `talking`, and `talker` are all fine. Same for plurals (`bird` → `birds`),
  `-ly` (`quick` → `quickly`), `-er`/`-est` (`big` → `bigger`/`biggest`), and
  irregular forms of listed words (`go` → `went`, `we` → `us`, `child` →
  `children`, `be` → `is`/`was`/`are`).
- **Nothing else is allowed.** If a word is not on the list and is not a form of
  a listed word, you may not use it — full stop — unless it is a technical term
  you handle the special way below.

There are two four-letter words that are very common but were left off the list
on purpose. Do not use them.

## The technical-term exception

Some things can't be named with simple words alone — a real place, a person's
name, or a needed science word like *photosynthesis* or *neuron*. You may use
such a term, but only if you:

1. **Introduce it with a plain description first**, then put the real term right
   after it, usually in round marks:
   *"the tiny power lines in your body's thinking parts (neurons)"*.
2. **Keep using the plain words after that** — the real term is just an anchor so
   the reader knows what thing you mean.
3. **Never let a technical term do the explaining for you.** The simple words
   still have to carry the meaning.

Use this sparingly. If you can avoid the hard word with a plain description, do.

## Required workflow — you MUST verify, not guess

You cannot tell by eye whether every word is on the list. Always check with the
script before you give the answer.

1. **Write** the explanation using only simple words (see the method below).
2. **Save it to a file** and run the checker:
   ```bash
   python3 scripts/check.py < draft.txt
   ```
   Or check a short piece directly:
   ```bash
   python3 scripts/check.py "your text here"
   ```
   For technical terms you have properly introduced, pass them so they aren't
   flagged:
   ```bash
   python3 scripts/check.py --allow "neuron,photosynthesis" < draft.txt
   ```
3. **Read the flags.** The script prints every word that is NOT allowed. For each
   flagged word, decide:
   - Is it a genuinely out-of-list word (like *convert*, *radiation*, *plant*)?
     → **Reword it** with simple words. (`convert` → `change`, `plant` →
     `green growing thing`.)
   - Is it a real technical term you meant to introduce and explain? → make sure
     you introduced it the plain-name way, then re-run with `--allow`.
4. **Fix and re-run** until the script says `CLEAN`.
5. **Only then give the answer** to the user (the clean prose, not the script
   output).

> The checker is a bit strict on purpose: it may flag an odd irregular form it
> doesn't know. Trust the rule ("same word, different form = one word") for those,
> but you must actually reword any word that is truly not a form of a listed word.
> When unsure whether a word is on the list, `grep -x -i theword references/word_list.txt`.

## How to write well inside the limit

Working in simple words is not "dumbing it down" — it's understanding the thing
well enough to say it plainly. The best simple explanations feel clear and even
a little full of wonder. Borrow this method:

1. **Give the thing a plain name, then anchor the real one.** Rename it the way a
   curious person would who'd never heard the official word, and put the real
   term in round marks the first time only.
2. **Open with what it IS and what it DOES** — one or two lines that give the
   reader the big picture before any details.
3. **Walk through the parts.** Every thing is made of smaller things doing jobs.
   Name each part simply and say what job it does and how it joins the others.
4. **Trace the chain of "this, which makes that."** Show cause and effect step by
   step: you push here → this part gets hot → that pushes the next part…
5. **Ground it** with a "why it matters" or "what would happen without it" line.
6. **End on something that makes the reader feel it** — a surprise, a size
   we can picture, or a small "oh, so that's how it works" moment.

Write in flowing lines, not lots of short bits with marks. Match the length to
how hard the thing is: a small everyday thing needs a few lines; a big system
(the inside of a star, how money moves) can take more.

### Words to reach for

When a big word wants to come out, swap it for a plain one already on the list.
A few common swaps:

- *utilize / employ* → **use**
- *require* → **need**
- *convert / transform* → **change** or **turn into**
- *approximately* → **about** or **around**
- *enormous / massive* → **huge** or **very big**
- *purchase* → **buy**
- *rotate / revolve* → **turn** or **spin**
- *consume* → **eat** or **use up**
- *observe* → **watch** or **see**
- *construct* → **build** or **make**

## Files in this skill

- `references/word_list.txt` — the full list of allowed base words (one per line).
  Read or `grep` this to settle any "is this word allowed?" question.
- `scripts/check.py` — the checker. Flags every word not on the list (handling
  normal and irregular word forms). `--allow "a,b"` whitelists introduced terms.
- `scripts/irregulars.json` — the map of irregular forms (went→go, was→be, …)
  the checker uses. You don't need to touch it.

## Quick self-check before you answer

- Did I run `check.py` and get `CLEAN`?
- Did I reword every truly out-of-list word instead of leaving it?
- For any technical term: did I give a plain name first and explain it in simple
  words, not lean on the term itself?
- Does the explanation actually make the reader *get it* — parts, process, and a
  bit of wonder — and not just sound simple?
