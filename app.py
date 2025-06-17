import streamlit as st
import openai

# ---------------- Sidebar ----------------
st.set_page_config(page_title="AI Prop Chatbot", layout="wide")
st.sidebar.title("🔐 OpenAI Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("ℹ️ Your key is used only in your session and not stored.")

# ---------------- Header ----------------
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🏡 AI Prop Chatbot</h1>
        <p style='font-size: 18px;'>Ask anything about real estate, properties, neighborhoods, deals, or investment strategies.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- Session ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- User Input ----------------
prompt = st.chat_input("Ask about a property (e.g., 'What’s the ARV for 123 Main St in Atlanta?')")

# ---------------- Function to Call OpenAI ----------------
def ask_openai_chat(user_question, api_key):
    try:
        openai.api_key = api_key
        system_prompt = """
        You are a real estate investment expert assistant named AI Prop Chat. 
        You help users analyze deals, estimate ARV, calculate ROI, provide local comps, and explain real estate terms in simple language. 
        Use real estate-specific language and give short, clear answers.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or gpt-3.5-turbo
            messages=messages,
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---------------- Process Prompt ----------------
if prompt and api_key:
    with st.spinner("Analyzing property..."):
        reply = ask_openai_chat(prompt, api_key)
        st.session_state.chat_history.append(("user", prompt))
        st.session_state.chat_history.append(("ai", reply))

# ---------------- Chat Display ----------------
for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("assistant"):
            st.markdown(message)

# ---------------- Footer ----------------
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray;'>
        <p>© 2025 AI Prop Chat. Powered by OpenAI.</p>
    </div>
""", unsafe_allow_html=True)

