import json
import os

import pymupdf
from openai import OpenAI

from system_prompt import SYSTEM_PROMPT

# PAPERS
HIGH_RIGOR_SCORE_PAPER = "data/attentionIsAllYouNeed.pdf"
LOW_RIGOR_SCORE_PAPER = "data/4821_a_simple_training_free_method_.pdf"

client = OpenAI(
    api_key=os.environ.get("BERGET_API_KEY"),
    base_url="https://api.berget.ai/v1",
)


def extract_text_from_pdf(pdf_path: str, max_pages: int = 15) -> str:
    """
    Extracts text and tables from a local PDF file using PyMuPDF.
    - Adds explicit page markers for precise claim location tracking.
    - Converts PDF tables into clean Markdown format for LLM readability.
    - Caps processing at max_pages to optimize token windows.
    """
    doc = pymupdf.open(pdf_path)
    pages_text = []

    for i, page in enumerate(doc[:max_pages]):
        # 1. Extract standard text
        text = page.get_text("text")

        # 2. Extract tables as Markdown (if any are present)
        table_texts = []
        tables = page.find_tables()
        if tables.tables:
            for t in tables:
                table_texts.append("\n[TABLE START]")
                table_texts.append(t.to_markdown())
                table_texts.append("[TABLE END]\n")

        # 3. Combine text and tables for the current page
        page_content = text + "\n".join(table_texts)
        pages_text.append(f"--- [PAGE {i + 1}] ---\n{page_content}")

    print(f"Successfully extracted {min(len(doc), max_pages)} pages from {pdf_path}.")
    return "\n".join(pages_text)


def audit_paper(pdf_path: str):
    # Step A: Get the structured text from PDF
    paper_text = extract_text_from_pdf(pdf_path)

    print("Sending text to Berget AI for claim auditing...")

    # Step B: Call Berget AI API
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Here is the text of the scientific paper to audit:\n\n{paper_text}",
            },
        ],
        response_format={"type": "json_object"},  # Forces clean JSON compliance
        temperature=0.0,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    try:
        audit_json_str = audit_paper(HIGH_RIGOR_SCORE_PAPER)

        # Pretty print the resulting JSON
        parsed_json = json.loads(audit_json_str)
        print("\n--- AUDIT REPORT SUCCESS ---")
        print(json.dumps(parsed_json, indent=2))

    except Exception as e:
        print(f"Error during audit: {e}")
