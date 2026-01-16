from dotenv import load_dotenv

load_dotenv()

"""
load env
accept a query
convery query into embeddings
retrive the relevant docs
pass these relevant docs as a system prompt to openai
get answer
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-5")
embeddings = OpenAIEmbeddings(model = "text-embedding-3-large", dimensions = 1024)


def chat_with_model(message: str):
    context = ""
    messages = [
    (
        "system",
        f"You are a helpful assistant that respond to the user query. you are given a context in the system prompt. you should use this context to provide an answer. context is following: {context}",
    ),
    ("human", f"${message}"),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

