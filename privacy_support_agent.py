from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools.retriever import create_retriever_tool

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
retriever = vectorstore.as_retriever(search_kwargs={"k" : 4})

kb_tool = create_retriever_tool(
    retriever=retriever,
    name="search_privacy_knowledge_base",
    description=(
        "Search several privacy policy, and terms and condition statements."
        " The search should be systematic. In that, that this tool should look out for"
        " clauses where the subject statement(s) are loosely or tightly defined. Positive"
        " points if tightly defined, negative if loosely defined. It should also look out for"
        " whether or not the subject statement(s) allow for data sharing or user tracking. Positive"
        " points if data sharing or user tracking is disallowed, negative otherwise. It should go"
        " deeper and check upto what extent data sharing and user tracking is being done. More "
        " tracking and sharing means more negative points, otherwise less negative points. Finally,"
        " the tool should be able to detect all PII being shared as well as location information."
    )
)
# 3. Bind the tool to the LLM
