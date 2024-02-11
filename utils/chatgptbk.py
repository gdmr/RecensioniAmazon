import os
import sys
import pandas as pd

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants

class Review:
    def __init__(self, text, date, title, stars, flavor):
        self.page_content = text
        self.date = date
        self.title = title
        self.stars = stars
        self.flavor = flavor
        self.metadata = {'date': date, 'title': title, 'stars': stars, 'flavor': flavor}

class CSVLoader:
    def __init__(self, directory):
        self.directory = directory

    def load(self):
        df = pd.read_csv(self.directory)
        for index, row in df.iterrows():
            yield Review(row['review_text'], row['review_date'], row['review_title'], row['review_stars'], row['review_flavor'])

def chat_model(filename, query):
    os.environ["OPENAI_API_KEY"] = constants.APIKEY

    current_path = os.getcwd()
    relative_path = os.path.join(current_path, 'data', filename)
    print("path relativa")
    print(relative_path)
    aggiunta = "Cercando sempre nelle recensioni, "
    querycompleta = aggiunta + query
    PERSIST = False

    if PERSIST and os.path.exists("persist"):
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = CSVLoader(relative_path)
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
      llm=ChatOpenAI(model="gpt-3.5-turbo"),
      retriever=index.vectorstore.as_retriever(search_kwargs={"k": 20}),
    )

    chat_history = []
    result = chain({"question": querycompleta, "chat_history": chat_history})

    return result['answer']
