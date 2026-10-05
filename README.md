# Actor Filmography Scraper

A Scrapy coursework project exploring filmography and potential co-actor data for **Eddie Murphy** and **Morgan Freeman**. It contains spiders for Wikipedia, IMDb, and Letterboxd, plus a saved JSON Lines export from Wikipedia.

Completed by **Shawn Tribuce** for **DS3500 — Homework 4**, the project demonstrates following links between pages, extracting HTML fields with CSS selectors, passing context through callbacks, and exporting structured records.

The saved output is a raw scraping dataset, not a validated co-actor network. The Wikipedia selector captures links beyond cast members, and further cleaning is needed before using the records as collaboration relationships.

## Repository Structure

```text
actor-filmography-scraper/
├── README.md
├── scrapy.cfg
├── actor_scrapper/
│   ├── __init__.py
│   ├── settings.py
│   ├── items.py
│   ├── pipelines.py
│   ├── middlewares.py
│   └── spiders/
│       ├── __init__.py
│       ├── wikipedia_spider.py
│       ├── imdb_spider.py
│       └── letterboxd_spider.py
├── data/
│   └── results.jsonl
└── docs/
    └── coursework_reflection.md
```

The package name `actor_scrapper` preserves the spelling referenced by the supplied configuration. The three spider files have been renamed for readability, and empty package initializer files have been added to restore the expected project layout. Existing Python source contents are unchanged.

The original assignment README is retained as `docs/coursework_reflection.md`, including its development reflection and AI-use disclosure. Submission metadata and the unrelated Boston 311 dashboard plan are excluded.

## Collection Workflow

Each spider starts from actor pages, follows links to individual works, and yields dictionaries containing four fields:

| Field | Intended meaning |
|---|---|
| `seed_actor` | Actor whose starting page led to the work |
| `movie_title` | Title extracted for the linked work |
| `co_actor` | Name or link title extracted from that work's page |
| `source` | `wikipedia`, `imdb`, or `letterboxd` |

These are intended field meanings rather than validated guarantees. In particular, `movie_title` can include non-film works, and `co_actor` can contain non-person links.

### Wikipedia

The spider starts from Eddie Murphy's filmography and Morgan Freeman's screen-and-stage page. It selects rows from `table.plainrowheaders`, follows the first matching `td i a` link, and passes the seed actor and link title to the next callback.

On each linked page, it scans list items under `div.mw-content-ltr.mw-parser-output` and uses the first linked title in each item as `co_actor`. This selector is not restricted to a Cast section, which explains why unrelated links appear in the export.

### IMDb

The spider attempts to follow filmography links and extract cast names from title pages. The saved dataset contains no IMDb records. The original reflection attributes the unsuccessful attempt to JavaScript-related extraction difficulties, but no crawl logs are included to establish the complete cause.

The source also contains an independent configuration issue: `allowed_domains` is set to `www.imbd.com`, while the starting URLs use `www.imdb.com`. That mismatch can prevent follow-up requests from being accepted by offsite filtering. It remains unchanged in the preserved source.

### Letterboxd

The spider attempts to follow film links from actor pages and extract names from the cast list. The saved dataset contains no Letterboxd records. The original reflection reports HTTP 403 responses; this review did not repeat those requests or independently verify the cause.

## Verified Dataset Profile

The supplied `results.jsonl` contains one JSON object per nonblank line.

| Measure | Value |
|---|---:|
| Total records | 33,088 |
| Wikipedia records | 33,088 |
| IMDb records | 0 |
| Letterboxd records | 0 |
| Records labeled Morgan Freeman | 22,577 |
| Records labeled Eddie Murphy | 10,511 |
| Distinct `movie_title` strings | 224 |
| Distinct complete records | 28,870 |
| Duplicate records beyond the first occurrence | 4,218 |
| Missing or empty values in the four exported fields | 0 |

Nonempty fields do not establish correctness. For example, `IMDb (identifier)` appears 203 times in the `co_actor` field, and other entries include `Rotten Tomatoes`, `ISBN (identifier)`, and television titles. The seed actors themselves also appear in that field.

These counts describe the supplied export. They should not be presented as counts of unique films, verified actors, or confirmed collaborations.

## Settings and Supporting Files

The supplied settings enable robots.txt handling with `ROBOTSTXT_OBEY = True`, set `CONCURRENT_REQUESTS_PER_DOMAIN = 1`, configure a one-second download delay, and specify UTF-8 feed export encoding. They also set a browser-style user agent.

These settings describe the code; they do not establish a site's current permissions or prove that every historical request was allowed. No live robots.txt review was performed for this repository preparation.

The other modules are mostly generated scaffolding:

- `items.py` defines an empty item class; spiders yield dictionaries directly.
- `pipelines.py` defines a pass-through pipeline. It is not enabled and does not clean or deduplicate records.
- `middlewares.py` contains pass-through middleware templates; the corresponding custom middleware settings are commented out.

There is no graph construction, network visualization, database integration, or dashboard implementation in the supplied project.

## Setup

Use Python 3 with Scrapy:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install scrapy
```

On Windows, activate the environment with `.venv\Scripts\activate`.

From the repository root, list the configured spiders:

```bash
scrapy list
```

The source defines the spider names `wikipedia`, `imdb`, and `letterboxd`.

### Inspect the saved data without crawling

```python
import json
from collections import Counter

with open("data/results.jsonl", encoding="utf-8") as file:
    records = [json.loads(line) for line in file if line.strip()]

print("Records:", len(records))
print("Sources:", Counter(row["source"] for row in records))
print("Seed actors:", Counter(row["seed_actor"] for row in records))
```

### Run a Wikipedia collection

After checking the target site's current access requirements and selectors, run from the repository root:

```bash
scrapy crawl wikipedia -O data/wikipedia_refresh.jsonl
```

This writes to a separate file, preserving the supplied `results.jsonl`; a later run with the same command overwrites `wikipedia_refresh.jsonl`. Current website markup can differ from the markup assumed by the spider. The preserved IMDb domain typo and historical Letterboxd failure should be addressed before treating those spiders as working collectors.

## Data Quality and Scope

The project needs additional validation before network analysis:

- Restrict extraction to actual cast entries and distinguish people from other linked entities.
- Separate films from television, music, and other works encountered in the starting tables.
- Remove duplicate records and decide whether seed-actor self-links belong in the output.
- Preserve source-page URLs and collection timestamps, which are absent from the current records.
- Check shared works across seed actors: the callbacks carry a seed actor, while duplicate request filtering can suppress a repeated request to the same work URL.

The current implementation has no item-level cleaning, entity resolution, or schema-validation stage. The original reflection's discussion of website access and failure causes is retained as historical context, not independently verified current guidance.

## Verification

During repository preparation, every nonblank JSONL line was parsed, source and actor counts were calculated, complete-record duplicates and empty fields were checked, and all seven supplied Python files passed syntax parsing.

The expected package layout was restored, but Scrapy execution and live crawls were not rerun. No automated test suite or saved crawl logs are included. The restored structure does not resolve the extraction-quality issues documented above.

## Author and Coursework

**Shawn Tribuce**  
**DS3500 — Homework 4**

See the original [coursework reflection](docs/coursework_reflection.md) for the author's account of implementation challenges and AI assistance.
