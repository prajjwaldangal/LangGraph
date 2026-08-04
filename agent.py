# 1. Define a LLM
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env file to get the openai key
load_dotenv()

# load the llm
llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
print(llm)

