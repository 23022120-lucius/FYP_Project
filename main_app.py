# main_app.py
import streamlit as st
import importlib

st.set_page_config(page_title="RALLY AI Multi-Profiler", layout="centered")

# --- Enhanced Custom CSS for a professional, modern look ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f7f9fa 0%, #e3eafc 100%);
    }
    .main {
        background-color: #fff;
        border-radius: 18px;
        padding: 2.5rem 2.5rem 1.5rem 2.5rem;
        box-shadow: 0 8px 32px rgba(0,87,184,0.10), 0 1.5px 6px rgba(0,0,0,0.04);
        margin-bottom: 2.5rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        transition: box-shadow 0.2s;
    }
    .main:hover {
        box-shadow: 0 12px 40px rgba(0,87,184,0.13), 0 2px 8px rgba(0,0,0,0.06);
    }
    .rally-logo {
        display: flex;
        align-items: center;
        margin-bottom: 2.2rem;
        margin-top: 0.5rem;
        justify-content: center;
        animation: fadeInLogo 1.2s cubic-bezier(.4,0,.2,1);
    }
    @keyframes fadeInLogo {
        0% { opacity: 0; transform: translateY(-20px);}
        100% { opacity: 1; transform: translateY(0);}
    }
    .rally-logo svg {
        height: 60px;
        width: 60px;
        margin-right: 1.2rem;
        filter: drop-shadow(0 2px 8px #0057B833);
        animation: pulseLogo 2.5s infinite alternate;
    }
    @keyframes pulseLogo {
        0% { transform: scale(1);}
        100% { transform: scale(1.07);}
    }
    .rally-title {
        font-size: 2.7rem;
        font-weight: 900;
        letter-spacing: 2px;
        color: #0057B8;
        margin-bottom: 0.2rem;
        text-shadow: 0 2px 8px #e3eafc;
    }
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0057B8;
        margin-top: 2.2rem;
        margin-bottom: 0.9rem;
        letter-spacing: 0.5px;
        text-align: left;
    }
    .divider {
        border-top: 2px solid #e0e0e0;
        margin: 2.2rem 0 1.5rem 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0057B8 60%, #0072ce 100%);
        color: white;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.7rem 2.2rem;
        border: none;
        margin: 0.7rem 0.7rem 0.7rem 0;
        font-size: 1.13rem;
        box-shadow: 0 2px 8px rgba(0,87,184,0.07);
        transition: background 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #003e7e 60%, #0057B8 100%);
        color: #fff;
        box-shadow: 0 4px 16px rgba(0,87,184,0.13);
    }
    .footer {
        text-align: center;
        color: #7a8ca3;
        font-size: 1.05rem;
        margin-top: 2.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.2px;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Custom Image Logo for RALLY AI ---
st.markdown('<div class="rally-logo">', unsafe_allow_html=True)
st.image('Screenshot 2025-07-21 160224.png', width=60)
st.markdown('<span class="rally-title">RALLY AI Multi-Profiler</span></div>', unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown('<div class="section-header">Choose a tool below to get started:</div>', unsafe_allow_html=True)
option = st.selectbox(
    "Select a tool:",
    ("Response Evaluator", "Business Profiling", "Consumer Profiling")
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if option == "Response Evaluator":
    st.markdown('<div class="section-header">Response Evaluator</div>', unsafe_allow_html=True)
    # Dynamically run ResponseEval.py
    spec = importlib.util.spec_from_file_location("ResponseEval", "ResponseEval.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
elif option == "Business Profiling":
    st.markdown('<div class="section-header">Business Profiling</div>', unsafe_allow_html=True)
    spec = importlib.util.spec_from_file_location("business", "business.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
elif option == "Consumer Profiling":
    st.markdown('<div class="section-header">Consumer Profiling</div>', unsafe_allow_html=True)
    spec = importlib.util.spec_from_file_location("consumer", "consumer.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    &copy; 2024 RALLY AI &mdash; All rights reserved.<br>
    Powered by <b>RALLY AI</b>
</div>
""", unsafe_allow_html=True)
