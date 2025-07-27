# rally_ai_ui_upgrade.py
import streamlit as st
import requests
import time
import pandas as pd
import os
import openpyxl
from datetime import datetime

# --- CSS Styling ---
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

# --- Header and Description ---
st.markdown("""
<div class="rally-logo">
<svg viewBox="0 0 60 60" fill="none">
  <circle cx="30" cy="30" r="28" fill="#0057B8" stroke="#003e7e" stroke-width="3"/>
  <text x="50%" y="54%" text-anchor="middle" fill="#fff" font-size="22" font-family="Arial" font-weight="bold" dy=".3em">R</text>
  <rect x="38" y="18" width="8" height="24" rx="4" fill="#fff" opacity="0.8"/>
  <rect x="14" y="18" width="8" height="24" rx="4" fill="#fff" opacity="0.8"/>
</svg>
<span class="rally-title">RALLY AI Business Profiling Optimizer</span>
</div>
""", unsafe_allow_html=True)

# --- Main Content ---
st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown('<div class="section-header">Business Profiling Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- LLM Configuration ---
llama_url = "http://localhost:11434/api/generate"
model = "llama3"
temperature = 0.2
top_k = 50
top_p = 0.9
num_predict = 300
gemini_key = "AIzaSyBOAAHCeDwtkBMsnfCGEQKaiJRu8DLdSlA"
groq_key = "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"

file_path = "business_profiling_llm.xlsx"

if "results" not in st.session_state:
    st.session_state["results"] = []

business_content = st.text_area("📄 Business Content (e.g. reviews, articles, transcripts)", height=200)
user_prompt = st.text_area("🧠 Prompt for Business Profiling (include your JSON instructions)", height=150)

col1, col2 = st.columns([1, 1])
with col1:
    run = st.button("🚀 Run")
with col2:
    save_excel = st.button("💾 Save to Excel")

# --- LLM Callers ---
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

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": f"Optimize this prompt for clarity and token efficiency:\n\n{prompt}"}]}]}
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            return f"[Gemini Error] {res.text}"
    except Exception as e:
        return f"[Gemini Exception] {e}"

def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a prompt optimizer."},
            {"role": "user", "content": f"Optimize this prompt for clarity and token efficiency:\n\n{prompt}"}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"[Groq Error] {res.text}"
    except Exception as e:
        return f"[Groq Exception] {e}"

def save_results_to_excel(results, file_path):
    columns = [
        "Response Time (s)",
        "Prompt Type",
        "Prompt",
        "Optimized Prompt",
        "Reply",
        "Token In",
        "Token Out",
        "Content"
    ]
    df_new = pd.DataFrame(results, columns=columns)
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

# --- Run Flow ---
current_run_results = []

if run and business_content and user_prompt:
    prompt_original = f"{user_prompt}\n\nExtract from this link:\n{business_content}"
    reply_original, token_in, token_out, duration = call_llama(prompt_original)
    st.divider()
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("🦙 Llama (Original Prompt)")
    st.code(reply_original, language="json")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state["results"].append({
        "Response Time (s)": duration,
        "Prompt Type": "Original",
        "Prompt": user_prompt,
        "Optimized Prompt": "",
        "Reply": reply_original,
        "Token In": token_in,
        "Token Out": token_out,
        "Content": business_content
    })
    current_run_results.append({
        "Response Time (s)": duration,
        "Prompt Type": "Original",
        "Prompt": user_prompt,
        "Optimized Prompt": "",
        "Reply": reply_original,
        "Token In": token_in,
        "Token Out": token_out,
        "Content": business_content
    })

    gemini_opt = call_gemini(user_prompt)
    reply_gemini, token_in_g, token_out_g, duration_g = call_llama(f"{gemini_opt}\n\nExtract from this link:\n{business_content}")
    st.markdown("<div class='result-card optimized'>", unsafe_allow_html=True)
    st.subheader("🔷 Llama (Gemini Optimized)")
    st.code(reply_gemini, language="json")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state["results"].append({
        "Response Time (s)": duration_g,
        "Prompt Type": "Gemini Optimized",
        "Prompt": user_prompt,
        "Optimized Prompt": gemini_opt,
        "Reply": reply_gemini,
        "Token In": token_in_g,
        "Token Out": token_out_g,
        "Content": business_content
    })
    current_run_results.append({
        "Response Time (s)": duration_g,
        "Prompt Type": "Gemini Optimized",
        "Prompt": user_prompt,
        "Optimized Prompt": gemini_opt,
        "Reply": reply_gemini,
        "Token In": token_in_g,
        "Token Out": token_out_g,
        "Content": business_content
    })

    groq_opt = call_groq(user_prompt)
    reply_groq, token_in_r, token_out_r, duration_r = call_llama(f"{groq_opt}\n\nExtract from this link:\n{business_content}")
    st.markdown("<div class='result-card optimized'>", unsafe_allow_html=True)
    st.subheader("🟧 Llama (Groq Optimized)")
    st.code(reply_groq, language="json")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state["results"].append({
        "Response Time (s)": duration_r,
        "Prompt Type": "Groq Optimized",
        "Prompt": user_prompt,
        "Optimized Prompt": groq_opt,
        "Reply": reply_groq,
        "Token In": token_in_r,
        "Token Out": token_out_r,
        "Content": business_content
    })
    current_run_results.append({
        "Response Time (s)": duration_r,
        "Prompt Type": "Groq Optimized",
        "Prompt": user_prompt,
        "Optimized Prompt": groq_opt,
        "Reply": reply_groq,
        "Token In": token_in_r,
        "Token Out": token_out_r,
        "Content": business_content
    })

# --- Summary Table ---
if current_run_results:
    st.markdown('<div class="summary-table">', unsafe_allow_html=True)
    st.markdown("### Summary Table")
    columns = [
        "Response Time (s)",
        "Prompt Type",
        "Prompt",
        "Optimized Prompt",
        "Reply",
        "Token In",
        "Token Out",
        "Content"
    ]
    df_summary = pd.DataFrame(current_run_results, columns=columns)
    st.dataframe(df_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Save Results to Excel ---
if save_excel and st.session_state["results"]:
    save_results_to_excel(st.session_state["results"], file_path)
    st.success("✅ Results saved to Excel successfully!")

st.markdown('</div>', unsafe_allow_html=True)
