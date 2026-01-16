from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
load_dotenv()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-5")
embeddings = OpenAIEmbeddings(model = "text-embedding-3-large", dimensions = 1024)


def chat_with_model(message: str):
    print("getting similar docs from RAG")
    context_result = vector_db.similarity_search(query=message)
    context = ""
    messages = [
    (
        "system",
        f"You are a helpful assistant that respond to the user query. you are given a context in the system prompt. you should use this context to provide an answer. context is following: {context_result}",
    ),
    ("human", f"${message}"),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

