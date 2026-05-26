# witchwell

Semantic search engine for Magic: The Gathering cards. Query by effect, mechanic,
or archetype rather than exact card name - powered by dense vector retrieval over
oracle text.

## How it works

1. Pull Scryfall `oracle-cards` JSON
2. Scryfall `oracle-cards` JSONL → filtered DataFrame (~34.5k cards, art series and tokens removed)
3. Each card is embedded as a structured sentence: `name | type_line | oracle_text`
4. Embeddings stored in Qdrant (768-dim cosine, nomic-embed-text-v1.5)
5. Queries are expanded for MTG jargon, then embedded with asymmetric search prefix

## Stack

- Python 3.13, uv
- [nomic-embed-text-v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) via sentence-transformers
- [Qdrant](https://qdrant.tech/) for vector storage and retrieval
- Pydantic v2 for data modeling

## Setup

project is still pre-MVP: it's close, but not ready to be set up yet

## Usage

```python
from witchwell.search import make_search_engine

engine = make_search_engine()
results = engine.search("destroy target creature", limit=10)
for r in results:
    print(r.score, r.card.name)
```

## Known limitations

- **Multi-intent queries** ("ramp into big creatures") resolve on one semantic center;
  retrieval quality degrades when query has two distinct intents.
- **Design pattern queries** ("aristocrats sacrifice outlet") find cards named after the
  archetype but miss unlabeled members. Tag-based filtering is a potential planned improvement.
- **Jargon coverage** is manually curated. Novel or niche terms may not expand correctly.

## Roadmap

- [ ] Eval suite (nDCG@5 across lexical / functional / jargon / design-pattern archetypes)
- [ ] Gradio UI + Hugging Face Spaces deploy
- [ ] Format and color identity filtering
- [ ] DFC image URI resolution
