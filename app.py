from langchain.vectorstores import Chroma
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from src.helper import load_embeddings, repo_ingestion
from dotenv import load_dotenv
import os
from flask import Flask, render_template, jsonify, request

load_dotenv()

app=Flask(__name__)


llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    max_retries=2,
    # other params...
)
embeddings=load_embeddings()
persist_directory='db'
vectordb=Chroma(persist_directory=persist_directory, embedding_function=embeddings)

delay=1
import time

def try_memory():
    while(True):
        try:
            memory=ConversationSummaryMemory(llm=llm, memory_key='chat_history', return_messages=True)
            if hasattr(memory, 'status_code') and memory.status_code == 429:
                time.sleep(delay)
                continue  # Retry the request
            return memory  # Return the answer if successful
        except Exception as e:
            print("exception occured: ", e)

def try_conversation_chain(input):
    while(True):
        try:
            qa=ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k":8}),memory=try_memory())
            result=qa(input)
            if hasattr(result, 'status_code') and result.status_code == 429:
                time.sleep(delay)
                continue  # Retry the request
            return result  # Return the answer if successful
        except Exception as e:
            time.sleep(delay)

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/chatbot',methods=['GET','POST'])
def gitRepo():
    if request.method=='POST':
        user_input=request.form['question']
        try:
            repo_ingestion(user_input)
        except Exception as e:
            print("Exception occured: {e}")
            print("Using default repo: https://github.com/Harshitnitw/End-to-End-Medical-Chatbot-Generative-AI")
            repo_ingestion("https://github.com/Harshitnitw/End-to-End-Medical-Chatbot-Generative-AI")
        os.system("python store_index.py")
        global vectordb
        vectordb=Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return jsonify({'response':str(user_input)})

@app.route('/get',methods=["GET","POST"])
def chat():
    input=request.form["msg"]
    print(input)
    if input=="clear":
        os.system("rm -rf repo")
        return "database cleared"
    result=try_conversation_chain(input)
    print("printed result is", result['answer'])
    return str(result["answer"])

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)