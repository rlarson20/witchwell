jupyter:
	~/src/bash/mk_uv_kernel.sh witchwell

qdrant-ping:
    curl -s "$QDRANT_URL/healthz"

qdrant-collections:
    curl -s "$QDRANT_URL/collections" \
      -H "api-key: $QDRANT_API_KEY" | python3 -m json.tool

push:
    git push
    git push space
