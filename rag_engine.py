import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain 
from langchain_classic.chains import create_retrieval_chain

def process_resume_and_roast(pdf_path, job_description):
    # 1. Ingestion: Load the PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # 2. Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    # 3. Embeddings & In-Memory Vector Store (FAISS)
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # We use a standard retriever here (k=4) since the document is small
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # 4. The LLM Brain
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7) # Slightly higher temp for a funnier "roast"
    
    # 5. The Secret Sauce: The Prompt
    system_prompt = (
        "You are an absolutely brutal, no-nonsense tech recruiter. "
        "Review the provided resume context against the following job description:\n"
        f"JOB DESCRIPTION:\n{job_description}\n\n"
        "You must output YOUR EXACT RESPONSE in this format:\n"
        "💀 Brutal overall verdict: \n"
        "🔴 3 things that will get you rejected: \n"
        "🟡 3 things that are painfully average: \n"
        "✅ 3 things that actually slap: \n"
        "🎯 Job match score (out of 10): \n"
        "💡 Rewritten bullet points (Give 2 examples in STAR format): \n"
        "🚀 30-day fix plan: \n\n"
        "Resume Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Roast my resume.")
    ])
    
    # 6. Build & Execute Chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)
    
    response = rag_chain.invoke({"input": "Roast my resume."})
    return response["answer"]