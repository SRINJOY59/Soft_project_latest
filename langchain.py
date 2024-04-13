# import sqlite3
# import pandas as pd
# import google.generativeai as genai

# # Google API Key setup
# GOOGLE_API_KEY = 'AIzaSyAaiMtEVHVzAtQ-6l2q2-nXTsMGBej0-Qc'  # Replace with your actual key
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel(model_name="gemini-pro")


# def connect_to_db(db_path):
#   """Connects to the sqlite database."""
#   conn = sqlite3.connect(db_path)
#   return conn


# def read_data(conn, query):
#   """Reads data from the database using a provided query."""
#   df = pd.read_sql_query(query, conn)
#   return df


# def close_connection(conn):
#   """Closes the connection to the database."""
#   conn.close()


# def generate_answer(query):
#   """Prompts the generative model to answer the question."""
#   context = """
#   You are an expert in handling orders and products in a dashboard system! 
#   There are two tables in the SQL database: `dashboard_order` and `dashboard_product`. 
#   Let's explore their attributes:

#   For `dashboard_order`:
#   - id
#   - order_quantity
#   - date
#   - status
#   - staff_id
#   - product_id

#   For `dashboard_product`:
#   - id
#   - name
#   - category
#   - quantity
#   - ordered_quantity
#   - buying_price
#   - selling_price
#   - total_selling_price
#   - profit
#   - barcode
#   - weight

#   You're now ready to write SQL queries based on these tables. For example, you could ask:

#   - How many products were ordered by a specific customer?
#   - What is the total price of all products in a certain category?
#   - Which product has the highest quantity?
#   If person asks for product names, then give their names not id

#   Feel free to craft SQL commands based on these tables and their attributes! 
#   """

#   prompt = f"{context}\nQuestion: {query}"
#   response = model.generate_content(prompt)
#   return response.text

# def read_sql_query(sql, db):
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     for row in rows:
#         print(row[0])
#     conn.close()



# answer = generate_answer("Which product has the highest quantity?")


# final = ""
# for i in range(len(answer)):
#    if i >= 6 and i < len(answer)-3:
#      final = final + answer[i]


# read_sql_query(final, "db.sqlite3")


import sqlite3
import pandas as pd
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from llama_index import VectorStoreIndex
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocesso
from langchain.text_splitter import RecursiveCharacterTextSplitter
import warnings
warnings.filterwarnings("ignore")




conn = sqlite3.connect("db.sqlite3")


query = "SELECT * FROM dashboard_product"


df = pd.read_sql_query(query, conn)

query1 = "SELECT * FROM dashboard_order"

df2 = pd.read_sql_query(query1, conn)


conn.close()

GOOGLE_API_KEY='AIzaSyBKYnycxw9NmVVVS9EsyuJuKie3zWeomwE'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name = "gemini-pro")


text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
context = "\n\n".join(str(df.iloc[i]) for i in range(len(df)))

context1 = "\n\n".join(str(df2.iloc[i]) for i in range(len(df2)))




texts = text_splitter.split_text(context)

texts1 = text_splitter.split_text(context1)

texts = texts + texts1

index=VectorStoreIndex.from_documents(texts,show_progress=True)

query_engine=index.as_query_engine()
r

retriever=VectorIndexRetriever(index=index,similarity_top_k=4)
postprocessor=SimilarityPostprocessor(similarity_cutoff=0.80)

query_engine=RetrieverQueryEngine(retriever=retriever,
                                  node_postprocessors=[postprocessor])