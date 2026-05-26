import json
from pathlib import Path

import pytest

from witchwell import make_search_engine


@pytest.fixture(scope="session")
def engine():
    return make_search_engine()


@pytest.fixture(scope="session")
def queries():
    return json.loads((Path(__file__).parent / "queries.json").read_text())
