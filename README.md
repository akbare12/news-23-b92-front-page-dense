# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b92-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b92-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page front page summing up 23 November 2026's world news in a single image:
31 stories across 6 regions.

## The day

- **AI rout hits Asia** — Kospi −3.3% closes 4,708.54, sheds 161 pts, intraday −5.8%;
  Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — Bridgetown summit, Barbados; 150 delegates
  back a risk framework, blueprint not treaty.
- **US lead over China at record low** — Asia Power Index 2026: US 78.9, China 73.6, gap 5.3,
  narrowest since 2018; US diplomatic influence −6 to 76.7; India 3rd 40.5.

Plus 10 more stories, 18 ALSO items, a world map with numbered pins, and a DATE CHECK box
that keeps 22/21/19 November stories out of the 23 November front page.

## How it is built

`draw.py` (Pillow) renders `entry.png` (1024×1024). `main.py` is stdlib-only: it validates
the PNG header and chunk CRCs by hand and copies the image to
`$MAKEFUN_OUTPUT_DIR/entry.png` — it never writes next to itself, so it also runs from a
read-only copy of the repo.

```sh
python3 draw.py            # regenerate entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # grader-style run
```

Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute
(Asia Power Index 2026). CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim,
not independently confirmed. All times UTC. Scenes are drawn illustrations, not photographs.
