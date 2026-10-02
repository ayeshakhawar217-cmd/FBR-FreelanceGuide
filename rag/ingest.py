from pathlib import Path
import hashlib
import re

import pymupdf

from rag.vectorstore import add_documents


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "fbr" / "documents"
PROCESSED_DIR = PROJECT_ROOT / "data" / "fbr" / "processed"


CHUNK_SIZE = 1800
CHUNK_OVERLAP = 300


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text while preserving useful legal wording.
    """

    text = text.replace("\x00", " ")

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
):
    """
    Split text into overlapping chunks.

    Overlap helps prevent important legal conditions
    from being separated between chunks.
    """

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def get_source_metadata(pdf_path: Path):
    """
    Assign source-level metadata based on filename.
    """

    filename = pdf_path.name.lower()

    if "ordinance" in filename:
        return {
            "source": "Income Tax Ordinance, 2001",
            "source_type": "primary_law",
            "authority": "FBR",
            "priority": 1,
        }

    if "financeact" in filename:
        return {
            "source": "Finance Act 2026",
            "source_type": "primary_law",
            "authority": "FBR",
            "priority": 1,
        }

    if "witholding" in filename or "withholding" in filename:
        return {
            "source": "FBR Withholding Tax Rate Card",
            "source_type": "rate_card",
            "authority": "FBR",
            "priority": 2,
        }

    return {
        "source": pdf_path.name,
        "source_type": "official_document",
        "authority": "FBR",
        "priority": 3,
    }


def create_id(source: str, page: int, chunk_index: int):
    raw = f"{source}-{page}-{chunk_index}"

    return hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()


def process_pdf(pdf_path: Path):

    print(f"\nProcessing: {pdf_path.name}")

    source_metadata = get_source_metadata(pdf_path)

    document = pymupdf.open(pdf_path)

    all_documents = []
    all_metadatas = []
    all_ids = []

    total_chunks = 0

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()

        text = clean_text(text)

        if not text:
            continue

        chunks = chunk_text(text)

        for chunk_index, chunk in enumerate(chunks):

            metadata = {
                **source_metadata,
                "filename": pdf_path.name,
                "page": page_number,
                "chunk_index": chunk_index,
            }

            chunk_id = create_id(
                pdf_path.name,
                page_number,
                chunk_index,
            )

            all_documents.append(chunk)
            all_metadatas.append(metadata)
            all_ids.append(chunk_id)

            total_chunks += 1

    document.close()

    if all_documents:

        add_documents(
            documents=all_documents,
            metadatas=all_metadatas,
            ids=all_ids,
        )

    print(
        f"Added {total_chunks} chunks "
        f"from {pdf_path.name}"
    )


def ingest_all_documents():

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    pdf_files = list(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:
        print(
            "No PDF files found in "
            f"{DOCUMENTS_DIR}"
        )

        return

    print(
        f"Found {len(pdf_files)} PDF documents."
    )

    for pdf_path in pdf_files:

        process_pdf(pdf_path)

    print("\nFBR knowledge base created successfully.")


if __name__ == "__main__":
    ingest_all_documents()