from src.helper import load_repo, text_splitter, load_embeddings
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
load_dotenv()

embeddings=load_embeddings()
documents=load_repo("repo/")
text_chunks=text_splitter(documents)

vectordb=Chroma.from_documents(text_chunks,embedding=embeddings,persist_directory='./db')
vectordb.persist()