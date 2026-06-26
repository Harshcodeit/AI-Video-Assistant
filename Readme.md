## 🏗️ Architecture

```
Video Upload
      │
      ▼
Audio Extraction
      │
      ▼
Video Chunking
      │
      ▼
Whisper Transcription
      │
      ▼
Transcript Chunking & Cleaning
      │
      ▼
Embedding Generation
      │
      ▼
ChromaDB (In-Memory Vector Store)
      │
      ▼
Semantic Retrieval
      │
      ▼
Sarvam AI LLM
      │
      ▼
Answer / Summary
```

---

## 🚀 How It Works

1. Users upload a video through the Streamlit interface.
2. The video is divided into smaller chunks to efficiently process long videos.
3. Audio is extracted from each chunk and transcribed using Whisper.
4. The generated transcripts are cleaned and split into semantic text chunks.
5. Embeddings are generated for each text chunk.
6. The embeddings are stored in an in-memory ChromaDB vector store.
7. For every user query, the system retrieves the most relevant transcript chunks using semantic similarity search.
8. The retrieved context is passed to the Sarvam AI LLM, which generates accurate, context-aware responses and summaries.
