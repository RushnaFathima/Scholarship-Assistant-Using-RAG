from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

from src.retriever import get_retriever

load_dotenv()


def answer_query(query: str):

    retriever = get_retriever()

    relevant_docs = retriever.invoke(query)

    if not relevant_docs:
        return "I don't have enough information to answer the query."

    combined_input = f"""
Based only on the following documents, answer the question.

Question:
{query}

Documents:
{chr(10).join([doc.page_content for doc in relevant_docs])}

If the answer is not found in the documents, say:
"I don't have enough information to answer the query."
"""

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.0,
    )

    messages = [
        SystemMessage(content="You are a experienced scholarship assistant."),
        HumanMessage(content=combined_input),
    ]

    result = llm.invoke(messages)

    return result.content