# witchwell — Design Decisions

## Embedding model: nomic-embed-text-v1.5 over all-MiniLM-L6-v2

**Chosen:** nomic-embed-text-v1.5 (768-dim, trust_remote_code=True)  
**Rejected:** all-MiniLM-L6-v2 (384-dim)

MiniLM smoke test showed Murder ("Destroy target creature") ranking 4th for the query "destroy target creature" - a literal match losing to paraphrases.
nomic moves Murder to 5th in a tighter score band (0.777–0.786 vs 0.677–0.707), with semantically correct cards above it. Issue: model quality

nomic-embed-text-v1.5 also supports asymmetric search via task prefixes
(`search_document:` / `search_query:`), which matches our use case: short natural
language queries against longer structured card text.

## Structured sentence format for document embeddings

Cards are embedded as: `name | type_line | oracle_text`

Rationale: oracle text alone loses card identity context; full payload fields (mana cost,
color identity, legalities) add noise to the embedding without improving retrieval quality
since those fields are for filtering, not semantic matching. The structured sentence keeps
the three fields the model needs to understand what a card _does_.

may come back to this one since some other fields are contextually relevant outside of being filters

## Jargon expansion at query time

MTG has a large domain-specific vocabulary ("ramp", "tutor", "blink", "wipe") with no
representation in the embedding model's training data.
Without expansion, "ramp" retrieves cards with "Rampaging" in their name.

The expansion layer (`jargon.py`) maps known terms to canonical oracle-text phrases before
embedding. This is applied at query time only - document embeddings are unchanged.

**Known tradeoff:** expansion is manually curated and brittle to novel jargon. A
domain-fine-tuned model would subsume this, but fine-tuning is post-MVP scope.
perfectly fine with doing that to be honest

**Multi-intent queries** ("ramp into big creatures") remain a known failure mode:
single-vector retrieval can only optimize for one semantic center.
Documented as a limitation; query decomposition is deferred.

## Scryfall filter strategy

Removed: `layout == art_series` and cards with "Token" in `type_line`.  
Retained: all other oracle cards including DFCs, adventures, and split cards.

DFC oracle text is joined as `face_a // face_b` at ingest time. Image URIs for DFCs
are currently `None` (images live on `card_faces[0]`); this is a known open item
for the UI layer, not retrieval.
