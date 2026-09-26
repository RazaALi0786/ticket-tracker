from dotenv import load_dotenv
load_dotenv()

# 1. Load the document
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("vpn_user_guide.pdf")
documents = loader.load()

# 2. Split the document into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

# 3. Create embeddings and build the FAISS vector store
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Save the vector store to disk
vectorstore.save_local("faiss_index")
print(f"Knowledge base created from {len(documents)} pages, {len(chunks)} chunks.")