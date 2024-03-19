from langchain.vectorstores import FAISS
from utils.openai_utils import get_openai

def load_faiss_retrieval() -> FAISS:
    _, embeddings = get_openai()

    #Load saved Faiss vectorstore
    index = FAISS.load_local("data", embeddings, allow_dangerous_deserialization=True)
    return index