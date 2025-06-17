import streamlit as st

# App title and logo
st.set_page_config(page_title="AI Prop Chat", layout="wide")

# Header section
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🏡 AI Prop Chat</h1>
    <h3 style='text-align: center;'>Smarter, Faster, and More Accurate than PropStream</h3>
    <p style='text-align: center; font-size:18px;'>
        AI-powered real estate platform that gives you the edge on every deal. 
        Chat with properties. Close with confidence.
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# 1. Comparison table
st.subheader("🔍 AI Prop Chat vs. PropStream")
comparison_data = {
    "Feature": ["AI Chat Assistant", "Property Owner Contact", "Real-Time Data", "Deal Analyzer", "Lead Scoring", "Comps Tool", "Export to CRM"],
    "AI Prop Chat ✅": ["Yes", "Yes", "Yes", "Advanced AI-Driven", "Smart Predictive", "Visual + AI Comps", "Direct Integrations"],
    "PropStream ❌": ["No", "Limited", "Delayed", "Basic ROI Only", "Manual", "Basic Filters", "CSV Download Only"]
}
st.table(comparison_data)

# 2. Feature grid
st.subheader("💡 Key Features of AI Prop Chat")
cols = st.columns(3)
features = [
    ("🧠 AI Chat with Properties", "Chat with any property to uncover investment insights instantly."),
    ("📊 Smart Deal Analyzer", "Automatically assess flips, rentals, or wholesale deals."),
    ("🏘️ Property Owner Lookups", "Instantly retrieve contact info & reach out."),
    ("📍 Visual Comps & Heatmaps", "See comparable sales with intelligent heatmaps."),
    ("📈 Predictive Lead Scoring", "Know which leads are most likely to close."),
    ("🔁 CRM + Workflow Integration", "Push hot leads to your favorite CRM automatically.")
]

for idx, (icon, desc) in enumerate(features):
    with cols[idx % 3]:
        st.markdown(f"### {icon}")
        st.markdown(desc)

st.markdown("---")

# 3. Demo Chat Box (AI Assistant placeholder)
st.subheader("🤖 Try the AI Prop Chat Assistant")
with st.chat_message("assistant"):
    st.markdown("Hi! I'm your AI Real Estate Assistant. Ask me anything about a property or deal!")
prompt = st.text_input("Ask about a property (e.g., 123 Main St)...")
if prompt:
    st.success(f"✅ Analyzing {prompt}...")
    st.info("🏡 This 3-bed property in Atlanta has an ARV of $285,000 and needs ~$25K in repairs. Ideal for flipping. 📈")

st.markdown("---")

# 4. Call to Action
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2>🚀 Ready to Level Up Your Real Estate Game?</h2>
        <p>Start using AI Prop Chat today – the smart way to find and close deals.</p>
        <a href="https://vipbusinesscredit.com/" target="_blank">
            <button style='padding: 10px 20px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;'>Sign Up Now</button>
        </a>
    </div>
""", unsafe_allow_html=True)

