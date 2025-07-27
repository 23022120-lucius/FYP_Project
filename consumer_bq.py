import streamlit as st
import requests
import time
import pandas as pd
import os
import openpyxl

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f7f9fa 0%, #e3eafc 100%);
    }
    .main {
        border-radius: 18px;
        padding: 2.5rem 2.5rem 1.5rem 2.5rem;
        box-shadow: 0 8px 32px rgba(0,87,184,0.10), 0 1.5px 6px rgba(0,0,0,0.04);
        margin-bottom: 2.5rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        transition: box-shadow 0.2s;
        background: none;
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

st.markdown("""
<div class="rally-logo">
<svg viewBox="0 0 60 60" fill="none">
  <circle cx="30" cy="30" r="28" fill="#0057B8" stroke="#003e7e" stroke-width="3"/>
  <text x="50%" y="54%" text-anchor="middle" fill="#fff" font-size="22" font-family="Arial" font-weight="bold" dy=".3em">R</text>
  <rect x="38" y="18" width="8" height="24" rx="4" fill="#fff" opacity="0.8"/>
  <rect x="14" y="18" width="8" height="24" rx="4" fill="#fff" opacity="0.8"/>
</svg>
<span class="rally-title">RALLY AI Consumer Behavioral Question Tester</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown('<div class="section-header">Consumer Behavioral Question Accuracy Testing</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

llama_url = "http://localhost:11434/api/generate"
model = "llama3"
temperature = 0.2
top_k = 50
top_p = 0.9
num_predict = 300
file_path = "consumer_bq_llm.xlsx"

if "results" not in st.session_state:
    st.session_state["results"] = []

user_profile = st.text_area("🧑 User Profile (JSON)", height=150)
behavioral_questions = st.text_area("📝 Behavioral Questions", height=120)
user_prompt = st.text_area("🧠 Prompt (Instructions for answering questions)", height=120)

col1, col2 = st.columns([1, 1])
with col1:
    run = st.button("🚀 Run Accuracy Test")
with col2:
    save_excel = st.button("💾 Save to Excel")

def call_llama(prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "num_predict": num_predict
    }
    start = time.time()
    try:
        res = requests.post(llama_url, json=payload)
        elapsed = time.time() - start
        if res.status_code == 200:
            data = res.json()
            return data.get("response", "").strip(), data.get("prompt_eval_count", ""), data.get("eval_count", ""), elapsed
        else:
            return f"[Llama Error] {res.text}", "", "", elapsed
    except Exception as e:
        return f"[Llama Exception] {e}", "", "", 0

current_run_results = []

if run and user_profile and behavioral_questions and user_prompt:
    prompt_full = f"{user_prompt}\n\nUSER PROFILE (JSON):\n{user_profile}\n\nBEHAVIORAL QUESTIONS:\n{behavioral_questions}"
    reply, token_in, token_out, duration = call_llama(prompt_full)
    st.divider()
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("🦙 Llama Response to Behavioral Questions")
    st.code(reply, language="json")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state["results"].append({
        "Response Time (s)": duration,
        "Prompt": user_prompt,
        "User Profile": user_profile,
        "Behavioral Questions": behavioral_questions,
        "Reply": reply,
        "Token In": token_in,
        "Token Out": token_out
    })
    current_run_results.append({
        "Response Time (s)": duration,
        "Prompt": user_prompt,
        "User Profile": user_profile,
        "Behavioral Questions": behavioral_questions,
        "Reply": reply,
        "Token In": token_in,
        "Token Out": token_out
    })

if current_run_results:
    st.markdown('<div class="summary-table">', unsafe_allow_html=True)
    st.markdown("### Results Table")
    columns = [
        "Response Time (s)",
        "Prompt",
        "User Profile",
        "Behavioral Questions",
        "Reply",
        "Token In",
        "Token Out"
    ]
    df_summary = pd.DataFrame(current_run_results, columns=columns)
    st.dataframe(df_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if save_excel and current_run_results:
    columns = [
        "Response Time (s)",
        "Prompt",
        "User Profile",
        "Behavioral Questions",
        "Reply",
        "Token In",
        "Token Out"
    ]
    df_new = pd.DataFrame(current_run_results, columns=columns)
    if os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_excel(file_path, index=False)
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    for col in ws.columns:
        for cell in col:
            cell.alignment = openpyxl.styles.Alignment(wrap_text=True)
    for col in ws.columns:
        max_len = max((len(str(cell.value)) if cell.value else 0) for cell in col)
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = min(max_len + 2, 60)
    wb.save(file_path)
    wb.close()
    st.success("✅ Results saved to Excel successfully!")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    &copy; 2025 RALLY AI &mdash; All rights reserved.<br>
    Powered by <b>RALLY AI</b>
</div>
""", unsafe_allow_html=True)
