from typing import cast

import pandas as pd

from witchwell.models import CardRecord, Legalities, QdrantPayload


def _nan_to_none(val):
    return val if pd.notna(val) else None


def get_data(path: str = "./data/oracle-cards-20260518212438.jsonl"):
    return pd.read_json(path_or_buf=path, lines=True)


def get_card_payload_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Filter raw Scryfall DataFrame to cards suitable for embedding.

    Removes art series and token layouts. Resolves DFC oracle text by
    joining face texts with ' // '. Returns a frame with only the columns
    needed for CardRecord construction.
    """

    filtered = df[
        (df["layout"] != "art_series")
        & (~df["type_line"].str.contains("Token", case=False, na=False))
    ].copy()

    def resolve_oracle_text(row):
        faces = row.get("card_faces")
        if isinstance(faces, list) and len(faces) >= 2:
            texts = [f.get("oracle_text", "") or "" for f in faces]
            return " // ".join(texts)
        return row.get("oracle_text")

    filtered["oracle_text"] = filtered.apply(resolve_oracle_text, axis=1)
    return cast(
        pd.DataFrame,
        filtered[
            [
                "id",
                "name",
                "image_uris",
                "color_identity",
                "legalities",
                "mana_cost",
                "type_line",
                "oracle_text",
                "prices",
                "scryfall_uri",
            ]
        ],
    )


def get_card_structured_sentences(frame):
    # frame must be from get_frame first: changed because don't want to call it twice
    return (
        frame["name"]
        + " | "
        + frame["type_line"]
        + " | "
        + frame["oracle_text"].fillna("")
    ).tolist()


def build_card_records() -> list[CardRecord]:
    """Build the full list of CardRecords from the Scryfall data file.

    Runs the full ingest pipeline: load → filter → structure sentences → compile.
    Expensive (~34.5k records); call once and reuse the result.
    """
    # 1. get raw data
    data = get_data()
    # 2. make filtered df and list of dicts
    filtered = get_card_payload_frame(data)
    rows = filtered.to_dict("records")
    # 3. make structured sentences
    sentences = get_card_structured_sentences(filtered)
    # 4. compile into list
    return [
        CardRecord(
            scry_id=row["id"],
            embedding_input=sentence,
            payload=QdrantPayload(
                name=row["name"],
                type_line=row["type_line"],
                oracle_text=_nan_to_none(row["oracle_text"]) or "",
                color_identity=row["color_identity"],
                legalities=Legalities(row["legalities"]),
                mana_cost=_nan_to_none(row["mana_cost"]),
                image_uris=_nan_to_none(row["image_uris"]),
                prices=row["prices"] or {},
                scryfall_uri=row["scryfall_uri"],
            ),
        )
        for row, sentence in zip(rows, sentences)
    ]
