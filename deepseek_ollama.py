import socket

import streamlit as st

from dotenv import load_dotenv # langfuse or opik
from langchain_ollama import ChatOllama

from langchain_core.prompts import (
                                        SystemMessagePromptTemplate,
                                        HumanMessagePromptTemplate,
                                        ChatPromptTemplate,
                                        MessagesPlaceholder
                                        )


from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

from langchain_core.output_parsers import StrOutputParser

load_dotenv('./../.env')

def chat_bot():
    st.title("Make Your Own Chatbot")
    st.write("Chat with me! Catch me at")

    base_url = "http://localhost:11434"
    model = 'deepseek-r1:1.5b'
    # check connection first.
    if not check_connection(host="localhost",port=11434):
        st.write("No connection to server")

    user_id = st.text_input("Enter your user id", "eg. basanta")

    def get_session_history(session_id):
        return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("Start New Conversation"):
        st.session_state.chat_history = []
        history = get_session_history(user_id)
        history.clear()

    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    ### LLM Setup
    llm = ChatOllama(base_url=base_url, model=model)

    system = SystemMessagePromptTemplate.from_template("You are helpful assistant.")
    human = HumanMessagePromptTemplate.from_template("{input}")

    messages = [system, MessagesPlaceholder(variable_name='history'), human]

    prompt = ChatPromptTemplate(messages=messages)

    chain = prompt | llm | StrOutputParser()

    runnable_with_history = RunnableWithMessageHistory(chain, get_session_history,
                                                       input_messages_key='input',
                                                       history_messages_key='history')

    def chat_with_llm(session_id, input):
        for output in runnable_with_history.stream({'input': input},
                                                   config={'configurable': {'session_id': session_id}}):
            if "<think>" in output and "</think>" in output:
                start = output.find("<think>")
                end = output.find("</think>") + len("</think>")
                yield output[:start] + "thinking..." + output[end:]
            else:
                yield output

    prompt = st.chat_input("What is up?")
    # st.write(prompt)

    if prompt:
        st.session_state.chat_history.append({'role': 'user', 'content': prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(chat_with_llm(user_id, prompt))

        st.session_state.chat_history.append({'role': 'assistant', 'content': response})


def check_connection(host="google.com", port=80, timeout=3):
    try:
        # Create a socket object
        socket.create_connection((host, port), timeout=timeout)
        print(f"Connection to {host}:{port} successful!")
        return True
    except socket.error as e:
        print(f"Connection to {host}:{port} failed: {e}")
        return False