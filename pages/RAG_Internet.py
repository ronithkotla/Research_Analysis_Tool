import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from scrapper import *
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="my_collection")



st.title("Research Internet ")




if "internet_form_submitted" not in st.session_state:
    st.session_state.internet_form_submitted=False
if "chat" not in st.session_state:
    st.session_state.chat=False


if "topic" not in st.session_state:
    st.session_state.topic=[]

    

if "images_on" not in st.session_state:
    st.session_state.images_on=[]

    

if "videos_on" not in st.session_state:
    st.session_state.videos_on=[]

    

if "pdfs_on" not in st.session_state:
    st.session_state.pdfs_on=[]
 

if "news_on" not in st.session_state:
    st.session_state.news_on=[]
if "links" not in st.session_state:
    st.session_state.links=[]

if "titles" not in st.session_state:
    st.session_state.titles=[]
if "snippets" not in st.session_state:
    st.session_state.snippets=[]



st.write("Everything you need from internet at one place.")
    
if not st.session_state.internet_form_submitted:
    with st.form("internet_form"):
        st.session_state.topic=st.text_input("Enter the topic to research")
        st.session_state.images_on=st.checkbox("Images")
        st.session_state.videos_on=st.checkbox("Videos")
        st.session_state.pdfs_on=st.checkbox("Books/materials")
        st.session_state.news_on=st.checkbox("Latest News")

        topic_submitted=st.form_submit_button("Submit")
        
        if topic_submitted:
            st.session_state.internet_form_submitted=True
            st.rerun()
            

            
if st.session_state.internet_form_submitted and not st.session_state.chat:
    
        info_box=st.info("Extracting Sources...")

        st.session_state.titles,st.session_state.links,st.session_state.snippets=get_search_links(st.session_state.topic)
        loader = UnstructuredURLLoader(urls=st.session_state.links)
        data=loader.load()
        if not data:
            raise ValueError("Error: No data was loaded from the URLs.")
        text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=2000
        )
        docs = text_splitter.split_documents(data)
        # Ensure `docs` is not empty
        if not docs:
            raise ValueError("Error: No documents were created after text splitting.")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        info_box.info("Converting to embeddings...")
        if "vectorstore" not in st.session_state:
            st.session_state.vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                collection_name="my_collection",
                client=chroma_client  # Use the new client instead of old settings
            )
        info_box.success("Successfully converted embeddings, now you can ask questions.")
        
        st.session_state.chat=True
        
if st.session_state.chat and st.session_state.internet_form_submitted:

        st.subheader("Extracted Search results from Internet:")

        for title,link,snippet in zip(st.session_state.titles,st.session_state.links,st.session_state.snippets):
            st.write(title)
            st.write(link)
            st.write(snippet)
            st.divider()

        if st.session_state.images_on:
            images=get_images(st.session_state.topic)
            if images: 
                st.subheader("Extracted images:")
                num_images = len(images)  # Get number of images
                num_cols = max(0, num_images)  # Set number of columns (max 4)
                
                cols = st.columns(num_cols)  # Create required columns dynamically
                
                for img, col in zip(images, cols):
                    with col:
                        st.image(img)
                st.divider()
            else:
                st.write("No images Found")

        if st.session_state.videos_on:
            videos=get_videos(st.session_state.topic)
            if videos: 
                st.subheader("Extracted Videos:")
                num_videos = len(videos)  # Get number of videos
                num_cols = max(0, num_videos)  # Set number of columns (max 4)
                
                cols1 = st.columns(num_cols)  # Create required columns dynamically
                
                for vid, col in zip(videos, cols1):
                    with col:
                        st.video(vid)
                st.divider()
            else:
                st.write("No videos Found")
        

        if st.session_state.pdfs_on:
            pdfs=get_pdfs(st.session_state.topic)
            st.subheader("Extracted Books/Materials:")
            if pdfs :
                for pdf in pdfs:
                    st.write(pdf)
                    st.divider()
            else:
                st.write("No Books/Materials Found")


        if st.session_state.news_on:
            news_titles,news_links,news_snippets=get_news(st.session_state.topic)
            st.subheader("Latest News :")
            if  news_titles and news_links and news_snippets:
                for news_title,news_link,news_snippet in zip(news_titles,news_links,news_snippets):
                    st.write(news_title)
                    st.write(news_link)
                    st.write(news_snippet)
                    st.divider()    
            else:
                st.write("No News Found")
        
        user_input=st.chat_input("Enter your question... or 'exit' ")
        if user_input:
            if user_input=="exit":
                st.session_state.internet_form_submitted=False
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


