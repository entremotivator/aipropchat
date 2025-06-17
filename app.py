import streamlit as st
import openai
from openai import OpenAI
from datetime import datetime

# ------------------ Streamlit Config ------------------
st.set_page_config(page_title="AI Prop Chat", layout="wide")

# ------------------ Sidebar Settings ------------------
st.sidebar.title("🔐 OpenAI Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
st.sidebar.markdown("---")
st.sidebar.markdown("ℹ️ Your key is used only in your session and not stored.")

# ------------------ Navigation ------------------
pages = [
    "🏠 Home", "📊 Comparison", "🚀 Features", "❤️ Testimonials", "💸 Pricing", "🤖 AI Chat", "📬 Contact"
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

# ------------------ Page: Testimonials ------------------
elif page == "❤️ Testimonials":
    st.markdown("## ❤️ What Users Are Saying")
    testimonials = [
        ("🗣️", "**'I used to spend hours researching properties. With AI Prop Chat, I just ask a question and get the full breakdown in seconds!'** – Jessica, Real Estate Investor"),
        ("🔥", "**'PropStream is good, but this is next level. Everything is faster, smarter, and easier.'** – Darnell, Wholesaler"),
        ("🚀", "**'I love the CRM export and AI-powered lead scoring. This tool helped me close 3 deals in 30 days.'** – Mike, Agent")
    ]
    for icon, quote in testimonials:
        st.markdown(f"{icon} {quote}")

# ------------------ Page: Pricing ------------------
elif page == "💸 Pricing":
    st.markdown("## 💸 Pricing Plans")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🆓 Starter")
        st.write("""
- 3 Property Lookups/Day  
- Limited AI Chat  
- No Export  
- Community Support  
**$0/month**
        """)
    with col2:
        st.markdown("### 💼 Pro")
        st.write("""
- Unlimited Lookups  
- Full AI Chat Access  
- CRM Integration  
- Export Capabilities  
**$99/month**
        """)
    with col3:
        st.markdown("### 🏢 Agency")
        st.write("""
- Team Access (5 users)  
- API Access  
- Advanced Analytics  
- Dedicated Support  
**$399/month**
        """)

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

