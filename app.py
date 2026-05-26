import gradio as gr

from witchwell import make_search_engine

engine = make_search_engine()


def search(query: str) -> list[list]:
    if not query.strip():
        return []
    return [
        [i + 1, round(r.score, 4), r.card.name, r.card.type_line, r.card.oracle_text]
        for i, r in enumerate(engine.search(query, limit=10))
    ]


with gr.Blocks(title="Witchwell") as demo:
    gr.Markdown("# Witchwell\nMTG semantic card search.")
    query_box = gr.Textbox(label="Query", placeholder="e.g. ramp into big creatures")
    search_btn = gr.Button("Search", variant="primary")
    results = gr.Dataframe(
        headers=["#", "Score", "Name", "Type", "Oracle Text"],
        datatype=["number", "number", "str", "str", "str"],
        wrap=True,
    )
    search_btn.click(fn=search, inputs=query_box, outputs=results)
    query_box.submit(fn=search, inputs=query_box, outputs=results)

if __name__ == "__main__":
    demo.launch()
