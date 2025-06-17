import streamlit as st
import openai
from openai import OpenAI

# ------------------ Streamlit Config ------------------
st.set_page_config(page_title="AI Prop Chatbot", layout="wide")
st.sidebar.title("🔐 OpenAI Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("ℹ️ Your key is used only in your session and not stored.")

# ------------------ App Header ------------------
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🏡 AI Prop Chatbot</h1>
        <p style='font-size: 18px;'>Ask anything about real estate, properties, neighborhoods, deals, or investment strategies.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------ Chat Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Chat Input ------------------
prompt = st.chat_input("Ask about a property (e.g., 'What’s the ARV for 123 Main St in Atlanta?')")

# ------------------ OpenAI Chat Function ------------------
def ask_openai_chat(user_question, api_key):
    try:
        client = OpenAI(api_key=api_key)

        system_prompt = """
        You are a real estate investment expert named AI Prop Chat.
        You help users analyze deals, estimate ARV, calculate ROI, provide local comps,
        and explain real estate terms in simple language. Give clear, helpful responses with real estate insight.
        """

        response = client.chat.completions.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ------------------ Handle User Input ------------------
if prompt and api_key:
    with st.spinner("Analyzing property..."):
        reply = ask_openai_chat(prompt, api_key)
        st.session_state.chat_history.append(("user", prompt))
        st.session_state.chat_history.append(("ai", reply))

# ------------------ Display Chat History ------------------
for role, message in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(message)

# ------------------ Footer ------------------
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray;'>
        <p>© 2025 AI Prop Chat. Powered by OpenAI.</p>
    </div>
""", unsafe_allow_html=True)

