import math


def dcg(relevant_at: list[int], k: int) -> float:
    return sum(rel / math.log2(rank + 2) for rank, rel in enumerate(relevant_at[:k]))


def ndcg_at_k(results: list[str], expected: list[str], k: int = 5) -> float:
    expected_rank = {name: len(expected) - i for i, name in enumerate(expected)}
    actual = [expected_rank.get(r, 0) for r in results[:k]]
    ideal = sorted(expected_rank.values(), reverse=True)
    idcg = dcg(ideal, k)
    return dcg(actual, k) / idcg if idcg > 0 else 0.0
