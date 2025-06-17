import streamlit as st
import openai
from openai import OpenAI
from datetime import datetime
import requests

# ------------------ Streamlit Config ------------------
st.set_page_config(page_title="AI Prop Chat", layout="wide")

# ------------------ Session State for Auth ------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ------------------ Login Screen ------------------
def login_screen():
    st.markdown("""
        <div style='text-align: center;'>
            <h1>🔐 Login to AI Prop Chat</h1>
        </div>
    """, unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            if username == "admin" and password == "password":  # Replace with real auth logic
                st.session_state.authenticated = True
                st.success("Login successful")
            else:
                st.error("Invalid credentials")

# ------------------ App Layout ------------------
if not st.session_state.authenticated:
    login_screen()
else:
    # ------------------ Sidebar Settings ------------------
    st.sidebar.title("🔐 OpenAI Settings")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    rentcast_api_key = st.sidebar.text_input("Enter RentCast API Key", type="password")
    st.sidebar.markdown("---")
    st.sidebar.markdown("ℹ️ Your keys are used only in your session and not stored.")

    # ------------------ Navigation ------------------
    pages = [
        "🏠 Home", "📊 Comparison", "🚀 Features", "❤️ Testimonials", "💸 Pricing",
        "🤖 AI Chat", "🏠 Property Records", "📬 Contact"
    ]
    page = st.sidebar.radio("Navigate", pages)

    # ------------------ Page: Home ------------------
    if page == "🏠 Home":
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1>🏡 AI Prop Chat</h1>
                <p style='font-size: 18px;'>Revolutionizing Real Estate. Smarter than PropStream. Built for modern investors, wholesalers, and agents.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("📘 About AI Prop Chat")
        st.write("""
            **AI Prop Chat** is an intelligent real estate data platform designed to simplify deal sourcing,
            automate property research, and optimize investment decisions with the power of artificial intelligence.

            Why limit yourself with old-school tools like PropStream? Our advanced chat-based interface gives you
            access to real-time insights, owner contact info, lead scoring, and predictive analysis — all in one place.
        """)

    # ------------------ Page: Comparison ------------------
    elif page == "📊 Comparison":
        st.subheader("📊 AI Prop Chat vs PropStream")
        comparison = {
            "Feature": [
                "AI Chat Assistant", "Real-Time Property Data", "Owner Contact Lookup",
                "Lead Scoring", "Comps & Heatmaps", "Smart Deal Analyzer",
                "CRM Export", "Mobile-Friendly", "AI Assistant Available 24/7"
            ],
            "AI Prop Chat ✅": [
                "Yes", "Yes", "Yes",
                "Predictive AI", "Interactive + Visual", "ARV + Repair Estimator",
                "Direct Integration", "Yes", "Yes"
            ],
            "PropStream ❌": [
                "No", "Delayed", "Limited",
                "Manual", "Basic Filters", "Basic ROI Calculator",
                "CSV Export", "Limited", "No"
            ]
        }
        st.table(comparison)

    # ------------------ Page: Features ------------------
    elif page == "🚀 Features":
        st.markdown("## 🚀 Core Features")
        feature_cols = st.columns(3)
        features = [
            ("🤖 AI Chat with Properties", "Get instant insights by chatting with any address."),
            ("📊 Smart Deal Analyzer", "Calculate ROI, ARV, and rehab instantly."),
            ("📞 Owner Contact Lookup", "Connect directly with motivated sellers."),
            ("📍 Visual Heatmaps & Comps", "See sales trends, price per sqft, and neighborhood dynamics."),
            ("⚡ Predictive Lead Scoring", "Prioritized leads that are more likely to convert."),
            ("🔁 CRM + Workflow Integration", "Push leads to your CRM in real-time."),
            ("📅 Task & Follow-Up Automation", "Schedule calls, texts, and emails from inside the app."),
            ("📱 Mobile App Ready", "Use anywhere. Mobile-friendly interface."),
            ("📂 Export & Custom Reports", "Build and share branded property reports.")
        ]
        for i, (title, desc) in enumerate(features):
            with feature_cols[i % 3]:
                st.markdown(f"### {title}")
                st.markdown(f"<div style='min-height: 80px;'>{desc}</div>", unsafe_allow_html=True)

    # ------------------ Page: Property Records ------------------
    elif page == "🏠 Property Records":
        st.markdown("## 🏠 Property Records Lookup")
        address_input = st.text_input("Enter a full property address")

        if st.button("Get Property Data") and rentcast_api_key and address_input:
            with st.spinner("Fetching property details..."):
                try:
                    response = requests.get(
                        "https://api.rentcast.io/v1/properties",
                        params={"address": address_input},
                        headers={"X-Api-Key": rentcast_api_key}
                    )
                    if response.status_code == 200:
                        prop = response.json()
                        st.json(prop)
                    else:
                        st.error(f"Failed to retrieve property. Status: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # ------------------ Page: AI Chat ------------------
    elif page == "🤖 AI Chat":
        st.markdown("## 🤖 Ask AI Prop Chat")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_prompt = st.chat_input("Ask about a property (e.g., 'What’s the ARV of 123 Main St in Atlanta?')")

        def ask_openai_chat(prompt, key):
            try:
                client = OpenAI(api_key=key)
                system_msg = """
                You are a real estate investment expert named AI Prop Chat.
                Help users analyze deals, estimate ARV, calculate ROI, provide local comps,
                and explain real estate terms in simple language.
                """
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"❌ Error: {str(e)}"

        if user_prompt and api_key:
            with st.spinner("Analyzing property..."):
                response = ask_openai_chat(user_prompt, api_key)
                st.session_state.chat_history.append(("user", user_prompt))
                st.session_state.chat_history.append(("ai", response))

        for role, msg in st.session_state.chat_history:
            with st.chat_message("user" if role == "user" else "assistant"):
                st.markdown(msg)

    # ------------------ Page: Contact ------------------
    elif page == "📬 Contact":
        st.markdown("## 📬 Get Started or Request a Demo")
        with st.form("lead_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            message = st.text_area("What are you looking for?")
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.success(f"Thanks {name}, we'll be in touch soon!")

    # ------------------ Footer ------------------
    st.markdown("""
        <hr style="margin-top: 50px;"/>
        <div style="text-align: center; color: gray;">
            <p>© {year} AI Prop Chat. All rights reserved.</p>
            <p><a href="https://vipbusinesscredit.com" target="_blank">Visit Website</a> | <a href="mailto:support@aipropchat.com">Contact Support</a></p>
        </div>
    """.format(year=datetime.now().year), unsafe_allow_html=True)
