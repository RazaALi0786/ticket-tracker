from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END


# 1. Define a LLM
#load .env file to get the openai key
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

#load the llm
llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
print(llm)


# 2. Load the knowledge base and create a retriever tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools.retriever import create_retriever_tool

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

kb_tool = create_retriever_tool(
    retriever,
    name="search_vpn_knowledge_base",
    description=(
        "Search Acme Corp's internal VPN user guide for installation steps, "
        "troubleshooting, and configuration details."
    ),
)

# 3. Bind the tool to the LLM
llm_with_tools = llm.bind_tools([kb_tool])

# 4. Define the Graph State
#line 2 of import - that's all we need

# 5. Create Graph Nodes
SYSTEM_PROMPT = """
You are a helpful IT support assistant for Acme Corp. \
You assist employees with VPN-related issues.
You have access to Acme Corp's internal VPN Knowledge Base through the \
search_vpn_knowledge_base tool - use it to find accurate, relevant answers \
to employee questions about installation, troubleshooting, or configuration.
Always respond clearly and politely.
Do not offer solutions unrelated to VPN.
"""

def chatbot(state: MessagesState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 4. Connect everything into a Graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=[kb_tool]))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
agent = graph_builder.compile()


if __name__ == "__main__":
    print("Agent ready. Type 'quit' to exit.\n")
    conversation = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            break
        conversation.append({"role": "user", "content": user_input})
        result = agent.invoke({"messages": conversation})
        conversation = result["messages"]
        print("Agent:", conversation[-1].content, "\n")