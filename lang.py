import sqlite3
import pandas as pd
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import warnings
warnings.filterwarnings("ignore")

GOOGLE_API_KEY='AIzaSyBKYnycxw9NmVVVS9EsyuJuKie3zWeomwE'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name = "gemini-pro")
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

def generate_vector_index():
    conn = sqlite3.connect("db.sqlite3")
    query = "SELECT * FROM dashboard_product"
    df = pd.read_sql_query(query, conn)
    query1 = "SELECT * FROM dashboard_order"
    df2 = pd.read_sql_query(query1, conn)
    conn.close()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    context = "\n\n".join(str(df.iloc[i]) for i in range(len(df)))
    context1 = "\n\n".join(str(df2.iloc[i]) for i in range(len(df2)))
    texts = text_splitter.split_text(context)
    texts1 = text_splitter.split_text(context1)
    texts = texts + texts1
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":1})
    return vector_index

def generate_answer(query):
  vector_index = generate_vector_index()
  relevant_documents = vector_index.get_relevant_documents(query)
  prompt_template = """"You are an expert in handling orders
   and products in a dashboard system! There are two tables 
   in the SQL database: `dashboard_order` and `dashboard_product`. 
   Let's explore their attributes:\n\nFor `dashboard_order`, 
   the attributes are:\nid,\norder_quantity,\ndate,status,\nstaff_id,\nproduct_id\n\n
   For `dashboard_product`, the attributes are:\n- id\n,name\n,category\n,quantity\n,ordered_quantity\n,buying_price\n,selling_price\n,total_selling_price\n,profit,barcode\n,weight\n\n
   ***Always refer to the product by its name, not its id.***\n\n
   You're now ready to answer questions based on these tables. 
   For example, you could ask:\n\n
   - How many products were ordered by a specific customer?\n
   - What is the total price of all products in a certain category?\n
   - Which product has the highest quantity?\n\n
   Feel free to craft answers based on these tables and their attributes! 
   ***If product is asked by the user, it is always product name, not id.***
   ***if anything outside the database is asked, then say "This query is not related to Product or Order Database".***
   ***Never write anything as Product (some number), always mention the name of the product whenever you refer to it***

Context: The user has shared the following information about their situation: {context}.

Question: The user is asking: {question}.

Answer:
"""

  prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
  stuff_chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
  stuff_answer = stuff_chain(
    {"input_documents": relevant_documents, "question":query}, return_only_outputs = True
    )
  return stuff_answer['output_text']

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row[0])
    conn.close()

answer = generate_answer("What is the most sold product?")
print(answer)

# final = ""
# for i in range(len(answer)):
#    if i >= 6 and i < len(answer)-3:
#      final = final + answer[i]

# read_sql_query(final, "db.sqlite3")