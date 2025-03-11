import streamlit as st
st.title("Research Analysis Tool🔍📚")
st.write("Choose your option:")
col1,col2,col3=st.columns(3,border=True)

with col1:
    st.write("Search and Scrap Websites:")
    st.page_link("pages/RAG_Internet.py", label="Internet Research", icon="🌎")

with col2:
    st.write("Research Local Folder and files:")
    st.page_link("pages/RAG_Local_Documents.py", label="Document Research", icon="📁")

with col3:
    st.write("Ask about anything quickly, Internet search and small file uploading options:")
    st.page_link("pages/Quick_Chat.py", label="Quick Chat", icon="🤖")

st.write("Know more about each tool below.")
st.divider()

st.subheader("Internet Search / RAG Internet")
st.write("1. Takes input a query from user.")
st.write("2. Searches over Google search results for websites, Images, Videos, Books/Materials, News via Google API and SerpAPI.")
st.write("3. Webscraping is performed only on websites using Unstructured Loader of Langchain.")
st.write("4. All the Scraped data is converted into embeddings using HuggingFace 'all-mpnet-base-v2' model.")
st.write("5. ChromaDB vector Database will store the vectors.")
st.write("6. This Vector Store is passed as retriever to LLM (Groq API- 'llama-3.3-70b-versatile').")
st.write("7. We can ask questions and LLM retrieves the Similar Text found with Sources.")
st.divider()


st.subheader("Document Research - RAG")
st.write("1. You can upload the Folder path containing PDFs, PDF path, Online PDF link .")
st.write("2. The text will be scraped and converted to embeddings using HuggingFace 'all-mpnet-base-v2' model.")
st.write("3. ChromaDB is used for storing the vectors.")
st.write("4. This Vector Store is passed as retriever to LLM (Groq API- 'llama-3.3-70b-versatile').")
st.write("5. We can ask questions and LLM retrieves the Similar Text found with Sources." )

st.divider()

st.subheader("Quick Search")
st.write("1. A normal LLM Chatbot with options to Access Internet Search results and Upload a small size pdf.")
st.write("2. Only Title, Link, Snippet is given to LLM as context ,Also Images, Videos, News, Books/Materials will be displayed as well.(Note:  Not a RAG).")
st.write("3. The file will be cleaned and only first 5000 words will be considered and given to LLM as context .(Note: Not a RAG).")
st.write("4. As RAG not is not implemented direct text is given as context making LLM responses faster.")
st.write("5. You can ask any questions related or unrelated to provided file/links")