# 1. For defining a LLM
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# 2. For defining the graph State
from langgraph.graph import MessagesState
# 3. For creating graph nodes
from langchain_core.messages import SystemMessage
# 4. Connect everything into a Graph
from langgraph.graph import StateGraph, START, END

"""
  |-----------|              |---------|              |-------|
  |  START    |  ----------> | CHATBOT |  --------->  |  END  | 
  |-----------|              |---------|              |-------|
"""

# Load .env file to get the openai key
load_dotenv()

# load the llm
llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
print(llm)


SYSTEM_PROMPT = """You are a privacy champion. Your ONLY responsibility is to assist anyone who cares about \
privacy with privacy-related issues. Always respond clearly and politely. If the user asks about privacy issues,
guide them by providing insights into the risks associated with their data such as PII.
If the user's question is NOT about privacy, DO NOT answer it. Instead, politely refuse and reply exactly
in this style:
"Sorry, I can only assist with privacy-related issues. Please ask me a question about data, and risks associated 
with the data. Do not provide any troubleshooting, suggestions, or information for non-privacy topics."
"""

def chatbot(state: MessagesState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages" : [response]}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
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
