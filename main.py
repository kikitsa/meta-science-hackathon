import json
import os
import time
from pathlib import Path

import pymupdf
from openai import OpenAI

from pdf_report import generate_audit_pdf
from system_prompt import SYSTEM_PROMPT

# PAPERS
HIGH_RIGOR_SCORE_PAPER = "data/attentionIsAllYouNeed.pdf"
LOW_RIGOR_SCORE_PAPER_1 = "data/4821_a_simple_training_free_method_.pdf"
LOW_RIGOR_SCORE_PAPER_2 = "data/6745_Learning_Deliberately_Act.pdf"
LOW_RIGOR_SCORE_PAPER_3 = "data/18694_Mechanistic_Interpretabi.pdf"


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
        model="google/gemma-4-31B-it",
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
    TARGET_PAPER = LOW_RIGOR_SCORE_PAPER_3
    print(f"Starting audit on: {TARGET_PAPER}")
    start_time = time.time()
    try:
        api_start = time.time()
        audit_json_str = audit_paper(TARGET_PAPER)
        api_duration = time.time() - api_start

        # Clean potential markdown wrappers and parse
        clean_json_str = (
            audit_json_str.strip().removeprefix("```json").removesuffix("```").strip()
        )
        parsed_json = json.loads(clean_json_str)

        # Dynamically create output filename based on input filename
        input_path = Path(TARGET_PAPER)
        output_filename = f"{input_path.stem}_audit_report.pdf"

        # Generate the PDF report
        generate_audit_pdf(parsed_json, output_filename)

        total_duration = time.time() - start_time

        print("\n--- AUDIT REPORT SUCCESS ---")
        print(f"Total claims extracted: {len(parsed_json.get('claims', []))}")
        print(f"Overall Rigor Score: {parsed_json.get('overall_rigor_score')}/10")
        print(f"📁 Report saved to: {output_filename}")
        print(f"⏱️ API Call Latency: {api_duration:.2f} seconds")
        print(f"⏱️ Total Pipeline Duration: {total_duration:.2f} seconds")
    except Exception as e:
        print(f"Error during audit: {e}")
