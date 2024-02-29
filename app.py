import streamlit as st
import openai

from langchain.vectorstores import FAISS
from langchain.memory import ConversationSummaryMemory
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain.prompts import MessagesPlaceholder
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor, create_openai_functions_agent

from utils.prompts import system_message
from utils.openai_utils import get_openai
from knowledge.retrievals import load_faiss_retrieval

st.set_page_config(
    page_title="Chat with the NYC Building Code Assistant!",
    page_icon="🏙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

openai.api_key = st.secrets.openai_key

st.title("Chat with the NYC Building Code Assistant! 💬")
st.info(
    "Let's get in touch! [Filip's LinkedIn](https://www.linkedin.com/in/szafranskifilip)",
    icon="💬",
)
if "messages" not in st.session_state.keys():  
# Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about the building code!",
        }
    ]

llm, embeddings = get_openai()

# Load and index data
@st.cache_resource(show_spinner=False)
def load_index():
    with st.spinner(
        text="Loading and indexing the building code docs – hang tight! This should take a moment."
    ):
        index = load_faiss_retrieval()
        return index

vectorstore = load_index()

# Set up the retriever
retriever = vectorstore.as_retriever()

tool = create_retriever_tool(
    retriever,
    "building_code_docs",
    "Search and return documents regarding building code, design and consturction issues. Input should be a fully formed question.",
)
tools = [tool]

memory_key="chat_history"
chat_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key=memory_key,
    return_messages=True,
    # output_key="answer",
    # buffer=context["buffer"],
    # prompt=CONVERSATION_SUMMARY_PROMPT_TEMPLATE,
)

prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

agent_engine = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent_engine,
    tools=tools,
    memory=chat_memory,
    verbose=True,
)
if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = agent_engine
if 'agent_executor' not in st.session_state:
    # Initialize 'agent_executor' and save it to the session state
    st.session_state.agent_executor = agent_executor
if prompt := st.chat_input(
    "Your question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent_executor.invoke({"input": prompt})
            st.write(response['output'])
            message = {"role": "assistant", "content": response['output']}

            # Add response to message history
            st.session_state.messages.append(message)