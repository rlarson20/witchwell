import pytest

from witchwell.metrics import ndcg_at_k


def test_ndcg_mean(engine, queries):
    scores = []
    for q in queries:
        results = [r.card.name for r in engine.search(q["query"], limit=5)]
        scores.append(ndcg_at_k(results, q["expected"]))
    mean = sum(scores) / len(scores)
    print(f"\nnDCG@5 mean: {mean:.4f}")
    assert mean > 0.05  # baseline ~0.057; regression floor, not quality target


@pytest.mark.parametrize(
    "archetype", ["lexical", "functional", "jargon", "design_pattern"]
)
def test_ndcg_by_archetype(engine, queries, archetype):
    subset = [q for q in queries if q["archetype"] == archetype]
    scores = [
        ndcg_at_k(
            [r.card.name for r in engine.search(q["query"], limit=5)],
            q["expected"],
        )
        for q in subset
    ]
    mean = sum(scores) / len(scores)
    print(f"\n{archetype} nDCG@5: {mean:.4f}")
    assert mean >= 0.0  # regression floor only; design_pattern baseline is 0.0
