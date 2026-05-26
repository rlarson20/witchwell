import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer

from witchwell.jargon import expand_jargon
from witchwell.models import QdrantPayload, SearchResult

load_dotenv()

COLLECTION_NAME = "mtg_cards_nomic"
QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")


class WitchwellSearch:
    """Vector search over the Qdrant card collection.

    Instantiate via make_search_engine() rather than directly.
    The model and client are held for the lifetime of the object;
    intended as a module-level singleton in serving contexts.
    """

    def __init__(
        self,
        client: QdrantClient,
        model: SentenceTransformer,
        collection: str,
    ) -> None:
        self.client = client
        self.model = model
        self.collection = collection

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search the card collection by natural language query.

        Applies jargon expansion before embedding. Returns results in
        descending score order; scores are cosine similarities in [0, 1].
        """

        vec = self.model.encode(
            f"search_query: {expand_jargon(query)}",
            normalize_embeddings=True,
        ).tolist()
        hits = self.client.query_points(
            collection_name=self.collection,
            query=vec,
            limit=limit,
        )
        return [
            SearchResult(
                scry_id=str(hit.id),
                score=hit.score,
                card=QdrantPayload.model_validate(hit.payload),
            )
            for hit in hits.points
        ]


def make_search_engine(
    qdrant_url: str = QDRANT_URL,
    qdrant_api_key: str | None = QDRANT_API_KEY,
    collection: str = COLLECTION_NAME,
    model_name: str = "nomic-ai/nomic-embed-text-v1.5",
) -> WitchwellSearch:
    """Construct a WitchwellSearch against a Qdrant Cloud cluster."""
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    if not client.collection_exists(collection):
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    model = SentenceTransformer(model_name, trust_remote_code=True)
    return WitchwellSearch(client=client, model=model, collection=collection)
