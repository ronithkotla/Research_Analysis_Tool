import streamlit as st
from scrapper import *
from groq import Groq
from pdfminer.high_level import extract_text


st.title("Quick Chat ")

st.write("Ask Anything you want")

if "start_page" not in st.session_state:
    st.session_state.start_page=True

if "internet_on" not in st.session_state:
    st.session_state.internet_on=False

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "stop" not in st.session_state:
    st.session_state.stop=False
if "user_input" not in st.session_state:
    st.session_state.user_input=""
def display_messages():
    st.session_state.chat_container = st.container()

    with st.session_state.chat_container:
        st.write("Starting new")
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div style='
                    display: flex; 
                    justify-content: flex-end; 
                    margin-bottom: 15px;
                    width: 100%;
                '>
                    <div style='
                        background-color: #414A4C; 
                        color: white;
                        border-radius: 15px;
                        padding: 12px 15px;
                        max-width: 80%;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        border-bottom-right-radius: 5px;
                    '>
                        <div style='
                            font-weight: 600; 
                            margin-bottom: 5px; 
                            color: #A0A0A0;
                            font-size: 0.8em;
                        '>You</div>
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            elif msg['role'] == 'assistant':
                st.markdown(f"""
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
                        '>Career Guidance Assistant</div>
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        
        st.session_state.internet_on=st.toggle("Search Internet")
        
        if st.session_state.stop:
            st.success("Conversation Ended successfully!")

def prompt_initialize():
    prompt="""
    You are a Chatbot , Help the user with whatever he asks kindly.
    """
    st.session_state.messages.append({"role":"system","content":prompt})
if st.session_state.start_page:

    prompt_initialize()
    st.session_state.start_page=False
    st.rerun()
def get_bot_response():
    client = Groq(
    api_key="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",
    )
    

    chat_completion = client.chat.completions.create(
        messages=st.session_state.messages,
        model="llama-3.3-70b-versatile",
    )
    bot_response=chat_completion.choices[0].message.content
    
    if bot_response:
        # Add user message to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Call the function to render messages
    display_messages()

def internet():
    with st.sidebar:
            titles,links,snippets=get_search_links(st.session_state.user_input)
            st.subheader("Extracted Search results from Internet:")
            st.session_state.messages.append({"role":"system","content":f"Use these links to respond if needed,which are from Internet:{titles,links,snippets}"})
            for title,link,snippet in zip(titles,links,snippets):
                st.write(title)
                st.write(link)
                st.write(snippet)
                st.divider()
            
            images=get_images(st.session_state.user_input)
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

            videos=get_videos(st.session_state.user_input)
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


            pdfs=get_pdfs(st.session_state.user_input)
            st.subheader("Extracted Books/Materials:")
            if pdfs :
                for pdf in pdfs:
                    st.write(pdf)
                    st.divider()
            else:
                st.write("No Books/Materials Found")

            news_titles,news_links,news_snippets=get_news(st.session_state.user_input)
            st.subheader("Latest News :")
            if  news_titles and news_links and news_snippets:
                for news_title,news_link,news_snippet in zip(news_titles,news_links,news_snippets):
                    st.write(news_title)
                    st.write(news_link)
                    st.write(news_snippet)
                    st.divider()    
            else:
                st.write("No News Found")

            st.session_state.internet_on=False

if not st.session_state.stop:

    if user_input := st.chat_input("Enter your answer or Type 'exit' ",accept_file=True,file_type="pdf"):
        st.session_state.user_input=user_input.text
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        if st.session_state.user_input=="exit":
            st.session_state.stop=True
            st.rerun()
        if user_input["files"]:

            file_text=extract_text(user_input["files"][0])
            print(file_text)
            file_text = re.sub(r'\s+', ' ', file_text).strip()
            print(file_text)
            file_text=file_text[:5000]
            print(file_text)
            st.session_state.messages.append({"role":"system","content":f"Use this pdf to answer, note that this might be just a part of file:{file_text}"})
            
                
        if st.session_state.internet_on :
            internet()

            
            
    get_bot_response()

