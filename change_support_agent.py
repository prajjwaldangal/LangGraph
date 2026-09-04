from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools.retriever import create_retriever_tool

"""
  |-----------|              |---------|              |-------|
  |  START    |  ----------> | CHATBOT |  --------->  |  END  | 
  |-----------|              |---------|              |-------|
                                  |
                                  |
                                  v
                             |---------|
                             |   Tool  |
                             |---------|  
"""

load_dotenv()
# 1. load the LLM
llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
print(llm)

# 2. Load the knowledge base and create a retriever tool
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

kb_tool = create_retriever_tool(
    retriever=retriever,
    name="search_privacy_knowledge_base",
    description=(
        "Search several terms and condition statements. ..."
        " The search should be systematic. In that, that this tool should look out for"
        " clauses where the subject statement(s) are loosely or tightly defined. Positive"
        " points if tightly defined, negative if loosely defined. It should also look out for"
        " whether or not the subject statement(s) allow for data sharing or user tracking. Positive"
        " points if data sharing or user tracking is disallowed, negative otherwise. It should go"
        " deeper and check upto what extent data sharing and user tracking is being done. More "
        " tracking and sharing means more negative points, otherwise less negative points. Finally,"
        " the tool should be able to detect all PII being shared as well as user location information."
    )
)
# 3. Bind the tool to the LLM
llm_with_tools = llm.bind_tools([kb_tool])


SYSTEM_PROMPT = """You are an information expert. Your ONLY responsibility is to assist anyone who cares about \
privacy with privacy-related issues. Always respond clearly and politely. If the user asks about privacy issues,
guide them by providing insights into the risks associated with their data such as PII.
If the user's question is NOT about privacy, DO NOT answer it. Instead, politely refuse and reply exactly
in this style:
"Sorry, I can only assist with privacy-related issues. Please ask me a question about data, and risks associated 
with the data. Do not provide any troubleshooting, suggestions, or information for non-privacy topics." 
The user will ask you question about a change they are going through. The change could be he/she/they are switching to 
a new cellular plan, a new housing lease, a new auto insurance, and so on and so forth. The change is not limited to 
just these but these are the common change scenarios you will be help them with. Let's call these states. So, the user 
is moving from an old state, that comprising of the old cellular plan, old housing lease, etc. to a new state, that 
comprising of the new cellular plan, new housing lease, etc. There could be multiple candidates for the new state. In 
 such a scenario your job is to help the make the best choice possible by understanding their old state and highlighting
 changes they could expect with the terms and conditions in the new state candidates.    
"""

def chatbot(state: MessagesState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


# 4. Define the graph state
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=[kb_tool]))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("chatbot", END)
agent = graph_builder.compile()
# 5.
