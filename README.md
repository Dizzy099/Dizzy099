<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=3200&pause=900&color=1A56A8&center=true&vCenter=true&width=720&lines=Backend+Engineer+%7C+Production+LLM+Systems;Python+%C2%B7+Django+%C2%B7+FastAPI+%C2%B7+Celery+%C2%B7+Node.js;Multi-provider+LLM+orchestration+%26+RAG;I+ship+the+unglamorous+parts+that+keep+AI+features+up" alt="Backend engineer, production LLM systems" />

### Awanish Mishra

**AI / LLM Application Engineer · Backend Engineer**

[![Email](https://img.shields.io/badge/Email-awanishmishra245@gmail.com-1A56A8?style=flat-square&logo=gmail&logoColor=white)](mailto:awanishmishra245@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-awanish--mishra-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/awanish-mishra-08aa0322a/)
[![Location](https://img.shields.io/badge/Noida,%20India-open%20to%20relocation-555?style=flat-square&logo=googlemaps&logoColor=white)](#)
[![GATE](https://img.shields.io/badge/GATE%20Qualified-Data%20Science%20%26%20AI%202025-success?style=flat-square&logo=google-scholar&logoColor=white)](#)

</div>

---

I build **production LLM systems**: multi-provider orchestration, RAG-backed knowledge workflows,
agentic tooling, and the backend infrastructure needed to ship AI features reliably.

Currently on the backend of **tingg.ai**, a multi-tenant AI content-generation SaaS. My focus is the
less glamorous half of AI engineering — routing, retries, evals, token/cost metering, idempotency,
feature flags and failure handling.

> Most of my strongest work lives in private employer repositories. What is public here is the
> smaller half: side projects, and the patterns I am rebuilding in the open.

## Tech

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

![Anthropic](https://img.shields.io/badge/Claude-D97757?style=for-the-badge&logo=anthropic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white)

</div>

## What I work on

```mermaid
flowchart LR
    Product[AI product feature] --> API[Python API layer]
    API --> Router[LLM provider router]
    Router --> Claude[Claude]
    Router --> OpenAI[OpenAI]
    Router --> Gemini[Gemini]
    Router --> DeepSeek[DeepSeek]
    API --> RAG[RAG / brand knowledge]
    API --> Agents[Tool-calling agents]
    API --> Jobs[Celery async jobs]
    Jobs --> Media[Image / video generation]
    API --> Metering[Token, cost, latency audit trail]
    API --> Flags[Feature flags and rollout controls]
```

## Production experience

**tingg.ai — multi-tenant AI content SaaS (backend)**

| What | Detail |
|---|---|
| Scale | ~200 REST endpoints, ~99 ORM models, 6 Django apps, a suite of 2,600+ tests |
| Orchestration | Multi-provider LLM routing with fallback across Claude, OpenAI, Gemini, DeepSeek |
| Workflows | DAG-based engine for LLM, image and video nodes — idempotent reruns, cancellation, async execution |
| Retrieval | RAG pipeline end to end: ingestion, chunking, extraction, tagging, distillation, weighted retrieval, context injection |
| Agents | Tool-registry conversational agent; autonomous template-authoring agent with validate/repair loops |
| Governance | Per-call token/cost/latency audit trails, append-only credit ledger, encrypted BYOK credentials |

**Freelance — [vatsaenterprises.in](https://vatsaenterprises.in)** · Node.js/Express/MongoDB + Angular

Payments (PhonePe), shipping integration, order and returns workflows, an auth-hardening pass that
closed a critical NoSQL-injection admin takeover, and a Lighthouse performance push
(catalogue 70 → 94, layout shift 0.75 → 0.02).

## Public projects

| Project | Stack | What it shows |
|---|---|---|
| [Glove Compliance Detection](https://github.com/Dizzy099/Glove-Compliance-Detection-System-) | Python, YOLOv8 | Computer-vision safety pipeline: batch inference, JSON logging, annotated outputs |
| [FastAPI Smart Banner](https://github.com/Dizzy099/Fastapi-Smart-Banner) | FastAPI | Clean API structure, request handling, deployment-ready patterns |
| [adFusion](https://github.com/Dizzy099/adFusion) | Python, JS | Ad recommendation prototype: personalisation and ranking logic |

## Writing

Notes from real production work, with proprietary details stripped out:

- Designing a multi-provider LLM fallback chain: what breaks in production
- RAG ingestion is five problems, not one — parse, chunk, extract, tag, distill
- Metering LLM cost per call: token audit trails and credit ledgers
- Agents that validate and repair their own output

## Background

`GATE Qualified — Data Science & AI (2025)` · `Harvard CS50x` · `B.Tech CSE, 80%`

## Open to

AI product teams where backend reliability matters as much as model capability — agent products,
RAG systems, LLM platforms, AI SaaS, workflow automation, and Python-heavy backend teams building
with LLMs.

<div align="center">

<img height="150" src="https://github-readme-stats.vercel.app/api?username=Dizzy099&show_icons=true&hide_border=true&title_color=1A56A8&icon_color=1A56A8&include_all_commits=true&count_private=true" alt="GitHub stats" />
<img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Dizzy099&layout=compact&hide_border=true&title_color=1A56A8&langs_count=8" alt="Top languages" />

<img src="https://github-readme-activity-graph.vercel.app/graph?username=Dizzy099&hide_border=true&color=1A56A8&line=1A56A8&point=1A56A8&area=true" alt="Contribution graph" width="90%" />

</div>
