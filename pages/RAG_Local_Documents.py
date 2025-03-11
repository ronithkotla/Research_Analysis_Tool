import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader



chroma_client = chromadb.PersistentClient(path="./chroma_db_folder")
collection = chroma_client.get_or_create_collection(name="my_collection_folder")



st.title("Research Local Documents")




if "chat_with_folder" not in st.session_state:
    st.session_state.chat_with_folder=False

if "local_form_submitted" not in st.session_state:
    st.session_state.local_form_submitted=False

if "light_page" not in st.session_state:
    st.session_state.light_page=False

if "docs" not in st.session_state:
    st.session_state.docs=[]


def gen_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    info_box.info("Converting to embeddings...")
    if "vectorstore" not in st.session_state :
        st.session_state.vectorstore = Chroma.from_documents(
            documents=st.session_state.docs,
            embedding=embeddings,
            collection_name="my_collection_folder",
            client=chroma_client  # Use the new client instead of old settings
        )
    info_box.success("Successfully converted embeddings, you can ask quesions now.")
    st.session_state.chat_with_folder=True

st.write("Ask questions on your files.")
    
if not st.session_state.local_form_submitted :
        with st.form("local_form"):
            st.write("Do you have a folder containing multiple files?")
            st.session_state.folder_path=st.text_input("Enter your folder path")
            
            
            st.write("Do you have a long pdf?")
            st.session_state.file_path=st.text_input("Upload your pdf path")
 
            st.write("Do you have an Online Pdf Link?")
            st.session_state.online_file_path=st.text_input("Upload your pdf link")


            topic_submitted=st.form_submit_button("Submit")
            
            if topic_submitted :
                st.session_state.local_form_submitted=True
                st.rerun()
            
            
if st.session_state.local_form_submitted and not st.session_state.chat_with_folder:
        info_box=st.info("Extracting information")
        if st.session_state.folder_path:
            loader = PyPDFDirectoryLoader(st.session_state.folder_path)
            
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
            )
            st.session_state.docs = text_splitter.split_documents(data)
            gen_embeddings()

        elif st.session_state.file_path:
            loader=PyPDFLoader(st.session_state.file_path)
            st.session_state.docs = loader.load_and_split()
            gen_embeddings()
        
        elif st.session_state.online_file_path:
            loader=OnlinePDFLoader(st.session_state.online_file_path)
            st.session_state.docs = loader.load()
            gen_embeddings()

        st.rerun()

if st.session_state.chat_with_folder and st.session_state.local_form_submitted:
        user_input=st.chat_input("Enter your question... or 'exit' ")
        if user_input:
            if user_input=="exit":
                st.session_state.local_form_submitted=False
                st.rerun()
            with st.chat_message("user"):
                st.write(user_input)

            llm=ChatGroq(api_key="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",model_name="llama-3.3-70b-versatile",temperature=0.1)
            
                   
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=st.session_state.vectorstore.as_retriever())
            result = chain.invoke({"question": user_input}, return_only_outputs=True)
            with st.chat_message("assistant"):
                st.markdown(
                    f"""
                        <div style='
                            display: flex; 
                            justify-content: flex-start; 
                            margin-bottom: 15px;
                            width: 100%;
                        '>
                            <div style='
                                background-color: #000000; 
                                color: white;
                                border-radius: 15px;
                                padding: 12px 15px;
                                max-width: 80%;
                                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                                border-bottom-left-radius: 5px;
                            '>
                                <div style='
                                    font-weight: 600; 
                                    margin-bottom: 5px; 
                                    color: #A0A0A0;
                                    font-size: 0.8em;
                                '>Researcher</div>
                                {result["answer"]}
                            
                        
                        """, unsafe_allow_html=True
                )
                # Display sources, if available
                sources = result.get("sources", "")
                if sources:
                    st.write("Answered from Sources:")
                    sources_list = sources.split("\n")  # Split the sources by newline
                    for source in sources_list:
                        st.write(source)


