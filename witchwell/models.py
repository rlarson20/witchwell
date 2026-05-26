from enum import StrEnum

from pydantic import BaseModel, RootModel


class Format(StrEnum):
    STANDARD = "standard"
    FUTURE = "future"
    HISTORIC = "historic"
    TIMELESS = "timeless"
    GLADIATOR = "gladiator"
    PIONEER = "pioneer"
    MODERN = "modern"
    LEGACY = "legacy"
    PAUPER = "pauper"
    VINTAGE = "vintage"
    PENNY = "penny"
    COMMANDER = "commander"
    OATHBREAKER = "oathbreaker"
    STANDARDBRAWL = "standardbrawl"
    BRAWL = "brawl"
    ALCHEMY = "alchemy"
    PAUPERCOMMANDER = "paupercommander"
    DUEL = "duel"
    OLDSCHOOL = "oldschool"
    PREMODERN = "premodern"
    PREDH = "predh"
    TLR = "tlr"


class Legality(StrEnum):
    BANNED = "banned"
    LEGAL = "legal"
    NOT_LEGAL = "not_legal"
    RESTRICTED = "restricted"


class Legalities(RootModel[dict[Format, Legality]]):
    def __repr__(self):
        return "{" + ", ".join(f"{k}: {v}" for k, v in self.root.items()) + "}"

    __str__ = __repr__

    def legal_in(self):
        active = {k: v for k, v in self.root.items() if v != Legality.NOT_LEGAL}
        return "{" + ", ".join(f"{k}: {v}" for k, v in active.items()) + "}"


class QdrantPayload(BaseModel):
    name: str
    type_line: str
    oracle_text: str
    color_identity: list[str]
    legalities: Legalities
    mana_cost: str | None
    image_uris: dict | None  # TODO: make this another class
    prices: dict
    scryfall_uri: str

    def full_repr(self):
        return f"Name: {self.name}\nType Line: {self.type_line}\nOracle Text: {self.oracle_text}\nColor Identity: {self.color_identity}\nLegalities: {self.legalities}\nMana Cost: {self.mana_cost}\nImage URIs: {self.image_uris}\nPrices: {self.prices}\nScryfall URI: {self.scryfall_uri}"  # noqa: E501

    def __repr__(self):
        return f"Name: {self.name}\nType Line: {self.type_line}\nOracle Text: {self.oracle_text}\nColor Identity: {self.color_identity}\nMana Cost: {self.mana_cost}\nScryfall URI: {self.scryfall_uri}"  # noqa: E501

    __str__ = __repr__


class CardRecord(BaseModel):
    scry_id: str
    embedding_input: str  # TODO: class for structured sentences
    payload: QdrantPayload

    def __repr__(self):
        return f"ID: {self.scry_id}\nStructured Sentence:\n{self.embedding_input}\nPayload:\n{self.payload}"  # noqa: E501

    __str__ = __repr__


class SearchResult(BaseModel):
    scry_id: str
    score: float
    card: QdrantPayload
