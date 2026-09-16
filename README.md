# DocMate — AI-Powered Document Assistant

**DocMate** is a conversational AI document assistant that lets users upload PDF and Word documents, ask questions about them, and have natural follow-up conversations with their content.

It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant sections from uploaded documents before generating an answer, while also providing **document and page-level source citations**.

🔗 **Live Demo:** https://docmate.streamlit.app/

---

## ✨ Features

* 📄 Upload **PDF and Word (.docx)** documents
* 💬 Ask questions about uploaded documents
* 🧠 Conversational follow-up questions
* 🔎 Semantic document search using embeddings
* 📚 Source and page-level citations
* 🤖 LLM-powered answers using Groq
* ⚡ Fast vector search using FAISS
* 🧩 Automatic document chunking
* 🌐 Live Streamlit deployment
* 😏 Conversational, witty AI personality

---

## 🛠️ Tech Stack

| Technology            | Purpose                              |
| --------------------- | ------------------------------------ |
| Python                | Core application                     |
| Streamlit             | Web interface and deployment         |
| LangChain             | RAG pipeline and document processing |
| Sentence Transformers | Text embeddings                      |
| FAISS                 | Vector similarity search             |
| Groq                  | LLM inference                        |
| PyPDF                 | PDF document loading                 |
| Docx2txt              | Word document loading                |

---

## 🧠 How It Works

DocMate follows a simple RAG pipeline:

```text
User uploads documents
        ↓
Document loading
        ↓
Text chunking
        ↓
Sentence Transformer embeddings
        ↓
FAISS vector index
        ↓
User asks a question
        ↓
Semantic similarity search
        ↓
Relevant document chunks
        ↓
Groq LLM
        ↓
Answer + source citations
```

The application preserves document metadata during the processing pipeline, allowing retrieved content to be traced back to its original document and page.

---

## 📂 Project Structure

```text
DocMate/
│
├── src/
│   ├── data_loader.py
│   ├── embedding.py
│   ├── vectorstore.py
│   └── search.py
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### Main Components

**`data_loader.py`**

Loads PDF and Word documents and converts them into LangChain documents while preserving their metadata.

**`embedding.py`**

Splits documents into smaller chunks and generates vector embeddings using Sentence Transformers.

**`vectorstore.py`**

Creates and manages the FAISS vector database used for semantic similarity search.

**`search.py`**

Handles document retrieval, conversation history, prompt construction, and LLM responses.

**`main.py`**

Provides the Streamlit interface where users upload documents and interact with DocMate.

---

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/DocMate.git
cd DocMate
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Or on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the application

```bash
streamlit run main.py
```

The application will open in your browser.

---

## 🔐 Environment Variables

DocMate requires the following environment variable:

```text
GROQ_API_KEY
```

Never commit your `.env` file or API keys to GitHub.

Make sure `.env` is included in your `.gitignore`:

```text
.env
__pycache__/
venv/
faiss_store/
data/uploads/
```

---

## 📖 Usage

1. Open DocMate.
2. Upload one or more PDF or Word documents.
3. Click **Process Documents**.
4. Ask a question about your documents.
5. Continue the conversation with follow-up questions.
6. Expand the **Sources** section to see where the answer came from.

For example:

```text
User:
What are the main objectives discussed in the document?

DocMate:
The document identifies three main objectives:
1. ...
2. ...
3. ...

📚 Sources
document.pdf — Page 4
document.pdf — Page 7
```

---

## 🎯 Why RAG?

A language model alone does not automatically know the contents of a user's private documents.

DocMate uses Retrieval-Augmented Generation to:

* Search the user's documents for relevant information.
* Provide that information to the LLM as context.
* Generate an answer grounded in the retrieved content.
* Preserve the original document metadata for source attribution.

This reduces the need for the model to rely solely on its pretrained knowledge when answering document-specific questions.

---

## 🔮 Future Improvements

Potential improvements include:

* [ ] Improved conversational query rewriting
* [ ] Better source deduplication
* [ ] Clickable document/page references
* [ ] Support for additional document formats
* [ ] Persistent document storage
* [ ] User authentication
* [ ] Streaming LLM responses
* [ ] Improved retrieval and reranking
* [ ] Multi-user document isolation

---

## 📌 Project Goals

DocMate was built to explore practical applications of:

* Retrieval-Augmented Generation
* Semantic search
* Vector databases
* LLM applications
* Document processing
* Conversational AI
* AI application deployment

The project focuses on building an end-to-end AI application rather than only experimenting with an isolated machine-learning model.

---

## 🌐 Live Demo

Try DocMate here:

**https://docmate.streamlit.app/**

---

## 👨‍💻 Author

**Ahmed Tolba**

Built with Python, LangChain, FAISS, Sentence Transformers, Groq, and Streamlit.
