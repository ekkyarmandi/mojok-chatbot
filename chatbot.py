import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from decouple import config


def get_ai_response(user_input, chat_history):
    ef = OpenAIEmbeddings(
        api_key=config("OPENAI_API_KEY"),
    )
    retriever = Chroma(
        persist_directory="mojok.co.db", embedding_function=ef
    ).as_retriever()
    llm = ChatOpenAI(api_key=config("OPENAI_API_KEY"))

    system_prompt = (
        "Gunakan konteks untuk menjawab pertanyaan. "
        "Kalau tidak tau, katakan tidak tau. "
        "Gunakan maksimal tiga kalimat dan jawab dengan tepat. "
        "konteks: {context}"
        "riwayat chat: {chat_history}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)
    output = chain.invoke({"input": user_input, "chat_history": chat_history})
    return output


st.set_page_config(page_title="Sedulur AI", page_icon="😌")
st.title("Sedulur AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage("Halo, saya Sedulur AI. Ada yang bisa saya bantu?")
    ]

for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("Human"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("AI"):
            st.write(msg.content)

user_input = st.chat_input("Masukkan pertanyaan kamu di sini")

if user_input and user_input != "":

    with st.chat_message("Human"):
        st.write(user_input)

    st.session_state.chat_history.append(HumanMessage(user_input))

    with st.chat_message("AI"):
        chat_history = st.session_state.chat_history
        output = get_ai_response(user_input, chat_history)
        ai_response = output.get("answer")
        st.write(ai_response)

    st.session_state.chat_history.append(AIMessage(ai_response))
