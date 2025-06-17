import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Prop Chat | Smarter Than PropStream", layout="wide")

# -------------------------------
# Hero Banner
# -------------------------------
st.markdown("""
    <style>
        .hero {
            background-color: #f0fdf4;
            padding: 50px 20px;
            border-radius: 12px;
            text-align: center;
        }
        .hero h1 {
            font-size: 48px;
            color: #2e7d32;
        }
        .hero p {
            font-size: 20px;
            color: #333;
        }
    </style>
    <div class="hero">
        <h1>🏡 AI Prop Chat</h1>
        <p>Revolutionizing Real Estate. Smarter than PropStream. Built for modern investors, wholesalers, and agents.</p>
    </div>
""", unsafe_allow_html=True)

# -------------------------------
# About Section
# -------------------------------
st.markdown("## 📘 About AI Prop Chat")
st.write("""
**AI Prop Chat** is an intelligent real estate data platform designed to simplify deal sourcing, automate property research, and optimize investment decisions with the power of artificial intelligence.

Why limit yourself with old-school tools like PropStream? Our advanced chat-based interface gives you access to real-time insights, owner contact info, lead scoring, and predictive analysis — all in one place.
""")

st.markdown("---")

# -------------------------------
# Comparison Table
# -------------------------------
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

# -------------------------------
# Feature Cards
# -------------------------------
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

for i, (title, description) in enumerate(features):
    with feature_cols[i % 3]:
        st.markdown(f"### {title}")
        st.markdown(f"<div style='min-height: 80px;'>{description}</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# Testimonials
# -------------------------------
st.markdown("## ❤️ What Users Are Saying")
testimonials = [
    ("🗣️", "**'I used to spend hours researching properties. With AI Prop Chat, I just ask a question and get the full breakdown in seconds!'** – Jessica, Real Estate Investor"),
    ("🔥", "**'PropStream is good, but this is next level. Everything is faster, smarter, and easier.'** – Darnell, Wholesaler"),
    ("🚀", "**'I love the CRM export and AI-powered lead scoring. This tool helped me close 3 deals in 30 days.'** – Mike, Agent")
]

for icon, quote in testimonials:
    st.markdown(f"{icon} {quote}")

st.markdown("---")

# -------------------------------
# Pricing Plans
# -------------------------------
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

st.markdown("---")

# -------------------------------
# AI Assistant Chat Simulation
# -------------------------------
st.markdown("## 🤖 Ask AI Prop Chat")
user_query = st.text_input("Ask a question (e.g., What’s the ARV of 456 Oak Street?)")
if user_query:
    st.success(f"✅ Processing your query: {user_query}")
    st.info("🏡 This 4-bed, 2-bath property in Houston, TX has an estimated ARV of $312,000. Repair costs are estimated at $28,000, with a flip ROI of 22%.")

st.markdown("---")

# -------------------------------
# Contact / Lead Form
# -------------------------------
st.markdown("## 📬 Get Started or Request a Demo")
with st.form("lead_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    message = st.text_area("What are you looking for?")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success(f"Thanks {name}, we'll be in touch soon!")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
    <hr style="margin-top: 50px;"/>
    <div style="text-align: center; color: gray;">
        <p>© {year} AI Prop Chat. All rights reserved.</p>
        <p><a href="https://vipbusinesscredit.com" target="_blank">Visit Website</a> | <a href="mailto:support@aipropchat.com">Contact Support</a></p>
    </div>
""".format(year=datetime.now().year), unsafe_allow_html=True)

