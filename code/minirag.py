import os
import time

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from openinference.instrumentation import using_session
from phoenix.otel import register

load_dotenv(".env_vars")

os.environ["TOKENIZERS_PARALLELISM"] = "false"


register(
    endpoint="http://localhost:6006/v1/traces",
    project_name="F-150 AI Assistant",
    auto_instrument=True,
)

RAG_PROMPT = """You are a knowledgeable automotive expert specializing in Ford vehicles. 
Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know.
Never make up an answer or reply from your own knowledge unless it is a simple greeting or small talk.
Always use the context to answer the question.

Context: {context}

Question: {question}

Answer:
"""


def collect_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag():
    loader = TextLoader(os.getenv("RAG_DATA_PATH"))
    print("Loading documents...")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, length_function=len, separators=["\n\n", "\n", " ", ""]
    )
    print("Splitting documents...")
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("Embedding documents...")
    vectorstore = FAISS.from_documents(texts, embeddings)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=RAG_PROMPT,
    )

    llm = ChatOpenAI(model="gpt-4o-mini")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    return (
        {
            "context": retriever | collect_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def main():
    session_id = str(time.time())
    rag = create_rag()

    print("-" * 80)
    print("Hello! I am your F-150 expert. Ask me anything! (type 'quit' to exit)")
    print("-" * 80)

    while True:
        question = input("? ").strip()
        if not question:
            continue
        if question.lower() in ["q", "quit", "exit", "bye"]:
            break
        with using_session(session_id):
            result = rag.invoke(question)
        print("> ", result)


if __name__ == "__main__":
    main()
