import os
import shutil
from pathlib import Path

import streamlit as st

from src.data_loader import load_all_documents
from src.search import RAGSearch


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="DocMate",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag" not in st.session_state:
    st.session_state.rag = None

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []


# --------------------------------------------------
# Temporary upload directory
# --------------------------------------------------

UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 DocMate — AI-Powered Document RAG Assistant")

st.write(
    """Chat with your documents using AI
        Upload PDFs or Word documents and ask questions,
        with citations showing exactly where the answer came from."""
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("📄 Documents")

    uploaded_files = st.file_uploader(
        "Upload your documents",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Upload PDF or Word documents."
    )

    process_button = st.button(
        "Process Documents",
        use_container_width=True
    )

    if uploaded_files:

        st.write(
            f"**{len(uploaded_files)} document(s) selected**"
        )

        for file in uploaded_files:
            st.caption(f"📄 {file.name}")


    st.divider()

    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# Process uploaded documents
# --------------------------------------------------

if process_button:

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF or Word document."
        )

    else:

        with st.spinner(
            "Processing your documents..."
        ):

            # Remove previous uploaded documents
            if UPLOAD_DIR.exists():

                for file in UPLOAD_DIR.iterdir():

                    if file.is_file():
                        file.unlink()

                    elif file.is_dir():
                        shutil.rmtree(file)

            # Save new uploaded documents
            for uploaded_file in uploaded_files:

                file_path = (
                    UPLOAD_DIR /
                    uploaded_file.name
                )

                with open(file_path, "wb") as f:
                    f.write(
                        uploaded_file.getbuffer()
                    )

            # Load documents
            documents = load_all_documents(
                str(UPLOAD_DIR)
            )

            if not documents:

                st.error(
                    "No readable documents were found."
                )

            else:

                try:

                    rag = RAGSearch()

                    rag.process_documents(
                        documents
                    )

                    st.session_state.rag = rag

                    st.session_state.documents_processed = True

                    st.session_state.uploaded_file_names = [
                        file.name
                        for file in uploaded_files
                    ]

                    # Start a new conversation
                    st.session_state.messages = []

                    st.success(
                        f"Successfully processed "
                        f"{len(uploaded_files)} document(s)."
                    )

                except Exception as e:

                    st.error(
                        f"An error occurred while processing "
                        f"the documents: {e}"
                    )


# --------------------------------------------------
# Show processed documents
# --------------------------------------------------

if st.session_state.documents_processed:

    st.subheader("Uploaded Documents")

    for filename in st.session_state.uploaded_file_names:

        st.write(f"📄 {filename}")

    st.divider()


# --------------------------------------------------
# Chat history
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # Display sources for assistant messages
        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                "📚 Sources"
            ):

                displayed_sources = set()

                for source in message["sources"]:

                    source_path = source.get(
                        "source",
                        "Unknown"
                    )

                    page = source.get(
                        "page"
                    )

                    # Get just the filename
                    filename = os.path.basename(
                        source_path
                    )

                    if page is not None:

                        # PyPDFLoader uses zero-based pages
                        page_number = page + 1

                        source_text = (
                            f"📄 **{filename}** "
                            f"— Page {page_number}"
                        )

                    else:

                        source_text = (
                            f"📄 **{filename}**"
                        )

                    # Avoid showing duplicate sources
                    source_key = (
                        filename,
                        page
                    )

                    if source_key not in displayed_sources:

                        st.write(
                            source_text
                        )

                        displayed_sources.add(
                            source_key
                        )


# --------------------------------------------------
# Chat input
# --------------------------------------------------

if st.session_state.documents_processed:

    user_query = st.chat_input(
        "Ask something about your documents..."
    )

    if user_query:

        # Display user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        with st.chat_message("user"):

            st.markdown(
                user_query
            )

        # Get response
        with st.chat_message("assistant"):

            with st.spinner(
                "Thinking..."
            ):

                try:

                    # Pass previous conversation
                    # BEFORE adding the new assistant response
                    chat_history = (
                        st.session_state.messages[:-1]
                    )

                    result = (
                        st.session_state.rag
                        .search_and_summarize(
                            user_query,
                            chat_history=chat_history,
                            top_k=5
                        )
                    )

                    answer = result["answer"]
                    sources = result["sources"]

                    st.markdown(
                        answer
                    )

                    # Display sources
                    if sources:

                        with st.expander(
                            "📚 Sources"
                        ):

                            displayed_sources = set()

                            for source in sources:

                                source_path = source.get(
                                    "source",
                                    "Unknown"
                                )

                                page = source.get(
                                    "page"
                                )

                                filename = os.path.basename(
                                    source_path
                                )

                                if page is not None:

                                    page_number = page + 1

                                    source_text = (
                                        f"📄 **{filename}** "
                                        f"— Page {page_number}"
                                    )

                                else:

                                    source_text = (
                                        f"📄 **{filename}**"
                                    )

                                source_key = (
                                    filename,
                                    page
                                )

                                if (
                                    source_key
                                    not in displayed_sources
                                ):

                                    st.write(
                                        source_text
                                    )

                                    displayed_sources.add(
                                        source_key
                                    )

                    # Save assistant response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:

                    st.error(
                        f"An error occurred: {e}"
                    )

else:

    st.info(
        "👈 Upload your PDF or Word documents "
        "from the sidebar and click **Process Documents** "
        "to start chatting."
    )