# The Digital Assets Framework Act, in plain words

A plain-language explainer of Australia's Corporations Amendment (Digital Assets Framework) Act 2026 for the Redbelly DAO community: what the Act is and why it was introduced, which businesses need a licence and which do not, the key dates, what it means for issuers using Tokeniser, and how Redbelly's identity and eligibility design measures up against the new rules, including the points no source settles.

**General information, not legal advice.**

Live site: https://australia-digital-assets-framework-ten.vercel.app

## Deliverables (TASK-30)

| Deliverable | Where |
| --- | --- |
| 1. The explainer | [PDF](public/downloads/digital-assets-framework-guide.pdf) · [Word](public/downloads/digital-assets-framework-guide.docx) · [Markdown](public/downloads/digital-assets-framework-guide.md) · [web page](public/index.html) |
| 2. Community summary and X thread | [Markdown](public/downloads/community-summary.md) · [web page](public/summary.html) |
| 3. Source list, with a link for every factual claim | [Markdown](public/downloads/source-list.md) · [web page](public/sources.html) |

## How the content is checked

Every factual statement in the explainer cites a passage from a source, and every passage is quoted word for word in the source list.

- `evidence/snapshots/` holds a plain-text copy of each source, taken on 25 October 2026. `evidence/manifest.json` records the link, the capture time and a SHA-256 fingerprint for each copy.
- `scripts/verify.py` fails the build if any of these is not true:
  - every saved copy still matches its SHA-256;
  - every quoted passage appears in its saved copy;
  - every citation points to a real passage, and every passage is cited;
  - every paragraph that states the law or reports a source carries a citation;
  - no sentence says Redbelly, Tokeniser or an issuer is licensed or compliant, and there is no price talk or investment advice;
  - there is no personal credit in the deliverables;
  - the explainer and the summary open with "not legal advice";
  - every post in the thread fits in 280 characters.
- `python3 scripts/verify.py --links` also requests every source link.
- The same check runs on every push (`.github/workflows/verify.yml`).

Primary sources come first: the Act as made, then the Government's own statement and ASIC's papers. Redbelly and Tokeniser pages are used only to report what those companies say about themselves. Text under "What the law says" and "What the companies say" reports the sources. Text under "What this means" and "Not settled" is analysis.

## Layout

```
content/
  sources.yaml     every source, numbered in this order
  evidence.yaml    the exact passages relied on, with where each sits in its source
  explainer.yaml   the explainer, with citations written {{passage-id}}
  summary.yaml     the community summary and the X thread
evidence/          saved copies of every source, and manifest.json
scripts/
  snapshot.py      save fresh copies of the sources
  verify.py        run every check above
  build.py         build the site and the PDF, Word and Markdown files
  assets.py        prepare fonts, logos, icons and the social card
public/            the published site (Vercel serves this folder)
```

## Build

```
pip install -r requirements.txt      # PyYAML is all that verify.py needs
npm install playwright                # for the PDF
python3 scripts/verify.py
python3 scripts/build.py              # needs pandoc for the Word file
```

To refresh the sources, run `python3 scripts/snapshot.py`, then `verify.py`. If a source has changed, the quote check shows exactly which passage no longer matches.

## Deploy

The site is static. On Vercel, import the repository and keep the defaults: `vercel.json` sets the output folder to `public/` and there is no build step. Any static host works the same way: publish the `public/` folder.

## Credits and licences

Fonts: Be Vietnam Pro and JetBrains Mono, SIL Open Font License 1.1 (see `licenses/`). Logo from the Redbelly DAO Task Board brand kit. Quoted passages remain the work of their publishers and are reproduced for reference with links to the originals.
