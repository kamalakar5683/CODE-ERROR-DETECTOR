import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDqui1f0QXykGcKYpHzZIlA16JLEQfLmzc")
llm = genai.GenerativeModel("models/gemini-1.5-flash")
code_review_bot = llm.start_chat(history=[])

# Set up Streamlit page configuration
st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🤖",
    layout="wide",
)

# Define custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.8rem;
        color: #3498db;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555555;
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar-content {
        font-size: 1rem;
        color: #333333;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #aaaaaa;
        margin-top: 40px;
        padding-top: 10px;
        border-top: 1px solid #ddd;
    }
    .chat-container {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .chat-human {
        color: #2c3e50;
    }
    .chat-ai {
        color: #16a085;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page header
st.markdown(
    """
    <div>
        <p class="main-title">🤖 AI Code Review Assistant</p>
        <p class="sub-title">Your AI-powered companion for reviewing code and suggesting improvements</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar content
with st.sidebar:
    st.header("Welcome! 👋")
    st.markdown(
        """
        This application helps you:
        - 🐛 Identify bugs in your code.
        - 🚀 Optimize and correct code snippets.
        - 💡 Improve your coding skills with AI guidance.
        """
    )
    st.markdown("#### 💻 Supported Languages:\n- Python\n- Java\n- C\n- C++")
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Code-icon.svg/120px-Code-icon.svg.png",
        width=150,
    )

st.markdown("---")

# Language selection
language = st.selectbox(
    "🌐 Select Programming Language:",
    ["Python", "Java", "C", "C++"],
    help="Choose the language of your code for review."
)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "text": (
                "Welcome! I can help review your code for bugs and provide suggestions. "
                "Select your language and paste your code below to get started."
            ),
        }
    ]

# Display previous chat messages
for message in st.session_state.messages:
    if message["role"] == "ai":
        st.markdown(f'<div class="chat-container chat-ai">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container chat-human">{message["text"]}</div>', unsafe_allow_html=True)

# Code input section
st.markdown(f"### ✏️ Paste Your {language} Code Below:")
code = st.text_area(f"{language} Code:", height=200, placeholder="Write or paste your code here...")

# Handle code submission
if st.button("🚀 Submit Code for Review"):
    if code.strip() == "":
        st.error("❌ Please paste your code before submitting.")
    else:
        st.session_state.messages.append({"role": "human", "text": code})
        st.markdown(f'<div class="chat-container chat-human">{code}</div>', unsafe_allow_html=True)

        with st.spinner("🧠 Analyzing your code..."):
            try:
                prompt = f"Review the following {language} code, identify potential bugs, and suggest fixes:\n\n{code}"
                response = code_review_bot.send_message(prompt)

                st.session_state.messages.append({"role": "ai", "text": response.text})
                st.markdown(f'<div class="chat-container chat-ai">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Developed using Streamlit & Generative AI 🤖</p>
    </div>
    """,
    unsafe_allow_html=True,
)
