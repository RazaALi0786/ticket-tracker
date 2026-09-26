from langchain_openai import ChatOpenAI

def create_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
    )

def build_prompt(
    question: str,
    context: str,
) -> str:

    return f"""
Answer the user's question using only the supplied context.

If the context does not contain enough information
to answer the question, say that you do not have
enough information.

Context:
{context}

Question:
{question}
"""

def generate_answer(
    question: str,
    context: str,
) -> str:

    llm = create_llm()

    prompt = build_prompt(
        question,
        context,
    )

    response = llm.invoke(prompt)

    return response.content