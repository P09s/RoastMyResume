# 🔥 RoastMyResume

> *Upload your resume. Brace yourself. Get hired.*

An AI-powered resume roasting tool that gives you **brutally honest feedback** before a recruiter rejects you. Built with LangChain RAG, Groq LLM, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-red)
![Groq](https://img.shields.io/badge/LLM-Llama%203.1-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What It Does

Upload your resume PDF + paste a job description → Get:

- 💀 **Brutal overall verdict**
- 🔴 **3 things that will get you rejected**
- 🟡 **3 things that are painfully average**
- ✅ **3 things that actually slap**
- 🎯 **Job match score out of 10**
- 💡 **Rewritten bullet points** (STAR format)
- 🚀 **30-day fix plan**

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Llama 3.1 8B via Groq API (free) |
| Embeddings | BAAI/bge-small-en-v1.5 (HuggingFace, free) |
| Vector Store | FAISS |
| RAG Framework | LangChain |
| UI | Streamlit |
| Deployment | Hugging Face Spaces |

**Total running cost = ₹0 / $0**

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/roast-my-resume.git
cd roast-my-resume
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
```bash
cp .env.example .env
# Add your Groq API key (free at console.groq.com)
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
roast-my-resume/
├── app.py              # Streamlit UI
├── rag_engine.py       # RAG pipeline (PDF loading, embeddings, chain)
├── requirements.txt    # Dependencies
├── .env.example        # API key template
└── README.md           # This file
```

---

## 🧠 How the RAG Pipeline Works

```
Resume PDF
    ↓
PyPDFLoader → loads all pages
    ↓
RecursiveCharacterTextSplitter → chunks(500, overlap=50)
    ↓
BAAI/bge-small-en-v1.5 → embeds each chunk
    ↓
FAISS vector store → stores + indexes embeddings
    ↓
Retriever (k=4) → fetches most relevant chunks
    ↓
Groq Llama 3.1 → generates roast using retrieved context
    ↓
Streamlit UI → displays formatted result
```

---

## 🔑 Get Your Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Create an API key
4. Add it to your `.env` file

---

## 🤝 Contributing

PRs welcome! Ideas for improvement:
- [ ] Add LinkedIn profile URL input
- [ ] Support DOCX format
- [ ] ATS (Applicant Tracking System) score
- [ ] Multi-language support (Hindi!)
- [ ] Email the roast report

---

## 📄 License

MIT License — use it, break it, improve it.

---

*Built by someone who got rejected too many times 💀*
