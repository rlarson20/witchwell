JARGON_MAP: dict[str, str] = {
    "ramp": "search your library for a basic land put it onto the battlefield add mana",
    "board wipe": "destroy all creatures exile all creatures",
    "wipe": "destroy all creatures",
    "tutor": "search your library for a card reveal it put it into your hand",
    "removal": "destroy target creature exile target creature",
    "counterspell": "counter target spell",
    "bounce": "return target permanent to its owner's hand",
    "blink": "exile target creature return it to the battlefield under its owner's control",  # noqa: E501
    "reanimate": "return target creature card from a graveyard to the battlefield",
    "reanimator": "return target creature card from a graveyard to the battlefield",
    "loot": "draw a card then discard a card",
    "cantrip": "draw a card",
    "aristocrats": "sacrifice a creature whenever a creature dies create a token",
    "wheels": "each player discards their hand and draws cards",
    "stax": "players can't untap permanents during their untap steps",
}


def expand_jargon(query: str) -> str:
    """Append oracle-text expansions for any recognized MTG jargon in query."""
    lower = query.lower()
    expansions = [exp for term, exp in JARGON_MAP.items() if term in lower]
    return query + " | " + " | ".join(expansions) if expansions else query
