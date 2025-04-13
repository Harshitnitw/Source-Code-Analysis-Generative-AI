import shutil
import os
from git import Repo
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain_mistralai import MistralAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain_mistralai.chat_models import ChatMistralAI
# from langchain.memory import ConversationSummaryMemory
# from langchain.chains import ConversationalRetrievalChain

def repo_ingestion(repo_url):
    if os.path.isdir("repo"):
        shutil.rmtree('repo')
    os.makedirs("repo", exist_ok=True)
    repo_path="repo/"
    Repo.clone_from(repo_url, to_path=repo_path)

def load_repo(repo_path):
    loader=GenericLoader.from_filesystem(
                                    repo_path,
                                    glob="**/*",
                                    suffixes=[".py"],
                                    parser=LanguageParser(language=Language.PYTHON,
                                    parser_threshold=500
                                    )
    )
    documents=loader.load()

    return documents

def text_splitter(documents):
    document_splitter=RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=500,
        chunk_overlap=20
        )
    text_chunks=document_splitter.split_documents(documents)
    return text_chunks

def load_embeddings():
    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
    )
    return embeddings