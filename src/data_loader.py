from pathlib import Path
from typing import List, Any

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader
)


def load_all_documents(data_dir: str) -> List[Any]:
    """
    Load PDF and Word documents from the specified directory.
    """

    data_path = Path(data_dir).resolve()
    documents = []

    # PDF files
    pdf_files = list(data_path.glob("**/*.pdf"))

    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_file))
            documents.extend(loader.load())
            print(f"[INFO] Loaded PDF: {pdf_file.name}")

        except Exception as e:
            print(f"[ERROR] Failed to load PDF {pdf_file}: {e}")

    # Word files
    docx_files = list(data_path.glob("**/*.docx"))

    for docx_file in docx_files:
        try:
            loader = Docx2txtLoader(str(docx_file))
            documents.extend(loader.load())
            print(f"[INFO] Loaded Word document: {docx_file.name}")

        except Exception as e:
            print(f"[ERROR] Failed to load Word file {docx_file}: {e}")

    return documents