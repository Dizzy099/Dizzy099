<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img src="assets/hero-light.svg" width="100%" alt="Awanish Mishra, backend engineer, Noida, India. I build the machinery behind AI products: LLM routing, async pipelines, billing that adds up. About 200 REST endpoints, 4 LLM providers, a suite of 2,600+ tests, Lighthouse score 70 to 94.">
</picture>

<p align="center">
  <a href="#what-ive-built"><b>What I've built</b></a> ·
  <a href="#bug-hunts"><b>Bug hunts</b></a> ·
  <a href="#where-ive-worked"><b>Where I've worked</b></a> ·
  <a href="#public-code"><b>Public code</b></a> ·
  <a href="#contact"><b>Contact</b></a>
</p>

When someone clicks **Generate** in an AI product, I build what runs next: the workflow engine,
the model calls that fail over when a provider goes down, the background jobs, and the ledger
that makes sure the bill is right.

> [!NOTE]
> Most of this runs in private company code, so it's shown here as diagrams and decisions. No
> proprietary code, data or client details.

## What I've built

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-engine-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-engine-light.svg">
  <img src="assets/card-engine-light.svg" width="100%" alt="01, tingg.ai, in production: multi-provider AI workflow engine. Workflows are graphs of LLM, image and video steps. When a provider fails, the call falls through to the next one: Claude returns 503, OpenAI answers, Gemini and DeepSeek stand by. A new model is an admin row, not a deploy. Django, Celery, 4 LLM APIs.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-video-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-video-light.svg">
  <img src="assets/card-video-light.svg" width="100%" alt="02, tingg.ai, generative video: idea to video, one scene at a time. Script, storyboard, frames and clips run as async jobs: submit, poll, store to S3. Scenes can be re-rolled, versioned, restored or cancelled. Each scene opens on the last frame of the one before.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-meter-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-meter-light.svg">
  <img src="assets/card-meter-light.svg" width="100%" alt="03, tingg.ai, usage and billing: every token has a price and an owner. Each model call records tokens, cost, latency and the run that spent it. Credits sit in an append-only ledger with a monthly allowance spent first and purchased credit kept until used. I found cache tokens billed at zero, fixed it, and re-priced history safely.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-autodm-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-autodm-light.svg">
  <img src="assets/card-autodm-light.svg" width="100%" alt="04, creator platform, automation: comment in, DM out, exactly once. Instagram webhooks trigger replies and DMs in real time. Each comment is claimed through a UNIQUE database column before the DM is sent, so a duplicate delivery is refused by the database. An hourly reconciler frees stuck claims. Built with several hundred unit tests.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-store-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-store-light.svg">
  <img src="assets/card-store-light.svg" width="100%" alt="05, freelance, live e-commerce: a live store, made fast and safe. Lighthouse performance on catalogue pages 70 to 94; layout shift 0.75 to 0.024. PhonePe payments, Shiprocket tracking, server-side pricing rules, a closed NoSQL-injection path to admin. 134 commits across 3 repos. Node.js, Express, MongoDB, Angular.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-router-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-router-light.svg">
  <img src="assets/card-router-light.svg" width="100%" alt="06, side project: do you even need a vector database? Routes document chunks to a taxonomy with embeddings, then benchmarks brute force against ChromaDB. Brute force is faster up to 2,400 vectors; ChromaDB wins at 24,000. Top-1 routing 69% semantic versus 31% lexical.">
</picture>

<sub>Card 06 is a from-scratch rebuild of a pattern I shipped at work, run on synthetic data. Its
repository isn't public yet.</sub>
<!-- TODO: once pushed, add: [chunk-router →](https://github.com/Dizzy099/chunk-router) -->

## Bug hunts

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/bugs-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/bugs-light.svg">
  <img src="assets/bugs-light.svg" width="100%" alt="Six production bugs and their fixes. 14 images instead of 7: a double-click race, fixed with row locks and idempotency keys. Every video request returned 500: a 480-second poll ran in a 120-second web worker, moved back onto Celery. Uploads stuck processing: a queue nobody consumed plus early acks, fixed with late acks and a stuck-job reaper. Costs drifting from prices: cache tokens priced at zero, fixed and history re-priced with a dry run first. Only the newest rule fires: wrong sort order, with tests proven to fail if the bug returns. Five auth flaws in my own feature: found in my own pre-release review and reported with fixes before merge.">
</picture>

<details>
<summary><b>Read the full story behind each bug</b></summary>

<br>

**14 images instead of 7.** Two requests raced through the same check-then-create path.
`select_for_update()` row locks and idempotency keys fixed it across generation, credit
purchases and workflow runs. That caused a follow-up bug: retrying a *failed* clip then
returned 409, because a stale lock was still held. So the lock now checks whether work is
really in flight before refusing. It also fails open on a database error, on purpose, and a test
covers that.

**Every video request returned 500.** It happened in one environment only.
`CELERY_TASK_ALWAYS_EAGER` ran a 480-second provider poll inside a Gunicorn worker that times
out at 120 seconds. I turned eager mode off and made a live worker consume that queue. I
rejected raising the timeout, because that only hides the problem and ties up web workers
for 8 minutes each.

**Uploads stuck in "processing".** Two causes were stacked:
- Tasks were routed to a queue no worker listened to.
- Tasks were acknowledged on pickup, so a crashed worker lost the job.

The fix has four parts:
- Queue names now come from one setting.
- `acks_late` with `reject_on_worker_lost`.
- A reaper that re-dispatches anything stuck for more than 15 minutes.
- An idempotent pipeline, so retries are safe.

**Costs drifting from prices.** Prompt-cache tokens were priced at zero, and some image prices
had drifted. I corrected the rates and built a reconciliation command that does a dry run
first. Rows with no recoverable source were left unattributed rather than guessed.

**Only the newest rule fires.** The resolver sorted candidate rules by `updated_at`
descending. I added five precedence tests. Putting the old sort order back makes all five fail,
so the tests can actually catch the bug.

**Five auth flaws in my own feature.** Before merging admin impersonation, I reviewed it myself
and found five flaws:
- A privilege escalation to superuser.
- Sessions that "stop impersonating" did not revoke.
- No expiry check on the token.
- Admins could grant the role to themselves.
- No time limit on a session.

I reported all five with fixes, and recommended shipping the feature switched off by default.

</details>

## Where I've worked

| When | Where | What |
|---|---|---|
| **Oct 2025 – now** | **The Higher Pitch**, Noida<br><sub>Associate Software Engineer</sub> | Backend for **tingg.ai** (cards 01–03), plus creator, music and education products (card 04). About 200 REST endpoints and 99 Django ORM models. |
| Apr – Sep 2025 | The Higher Pitch<br><sub>Software Engineer Intern</sub> | Django services, including an API gateway fronting 40+ endpoints across six apps |
| **Sep 2026 – now** | **Vatsa Enterprises**<br><sub>Freelance, full-stack</sub> | [vatsaenterprises.in](https://vatsaenterprises.in) (card 05) |
| Jan 2024 – Mar 2025 | Vatsa Enterprises<br><sub>Software Developer Intern</sub> | PHP/MySQL store rebuild; RPA automation that roughly halved manual work (my own estimate) |

<sub>B.Tech CSE, Dr. Rammanohar Lohia Avadh University (2021–25) · GATE qualified, Data Science
& AI (2025) · Harvard CS50x · 5th rank, college hackathon</sub>

## Public code

Smaller than the systems above, and honest about what's finished.

| Repo | What it does |
|---|---|
| **[Smart Banner](https://github.com/Dizzy099/Fastapi-Smart-Banner)**<br><sub>FastAPI · Gemini · Pillow</sub> | Turns a product photo and a logo into a banner. Gemini plans the layout as JSON, Pillow renders it, and a second Gemini call critiques legibility (logged only, for now). |
| **[Glove Compliance](https://github.com/Dizzy099/Glove-Compliance-Detection-System-)**<br><sub>YOLOv8 · OpenCV</sub> | Checks images for gloved or bare hands. YOLOv8 finds people, then a colour, texture and edge score classifies each hand. Includes its own overlap filter (NMS) and a parallel batch CLI. |
| **[adFusion](https://github.com/Dizzy099/adFusion)**<br><sub>Django · React · TinyLlama</sub> | Ad-copy generator running a 1.1B-parameter model locally on CPU. Parses the model's output into structured fields, with a template fallback when parsing fails. |

## Stack

<img src="assets/stack-icons.svg" height="40" alt="Python, Django, FastAPI, MySQL, PostgreSQL, RabbitMQ, Docker, AWS, Jenkins, Git">

**Daily:** Python · Django/DRF · Celery · RabbitMQ · MySQL · Docker · Jenkins · AWS (EC2, S3) ·
Claude, OpenAI, Gemini and DeepSeek APIs · pytest · Ruff · Mypy<br>
**Also shipped with:** Node.js/Express · MongoDB · Angular · React · Meta Graph API · PhonePe · Shiprocket

## Contact

I'm looking for **backend and AI-backend roles**: teams where the model is one dependency and
the job is making everything around it dependable. I'm in Noida and open to relocation.

<a href="mailto:awanishmishra245@gmail.com"><img src="https://img.shields.io/badge/Email-awanishmishra245%40gmail.com-0969da?style=for-the-badge&logo=gmail&logoColor=white" alt="Email awanishmishra245@gmail.com"></a>
<a href="https://www.linkedin.com/in/awanish-mishra-08aa0322a/"><img src="https://img.shields.io/badge/LinkedIn-Awanish%20Mishra-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn: Awanish Mishra"></a>
