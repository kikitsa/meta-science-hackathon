import pymupdf
from system_prompt import SYSTEM_PROMPT


# PAPERS
HIGH_RIGOR_SCORE_PAPER = "data/attentionIsAllYouNeed.pdf"
LOW_RIGOR_SCORE_PAPER = "data/4821_a_simple_training_free_method_.pdf"


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


# Quick test snippet
extracted_content = extract_text_from_pdf(LOW_RIGOR_SCORE_PAPER)
# print(extracted_content[:1000])
