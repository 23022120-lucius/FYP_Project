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
    .stTextArea textarea {
        background: #f4f8fd;
        border-radius: 10px;
        border: 1.5px solid #e3eafc;
        font-size: 1.12rem;
        min-height: 90px;
        transition: border 0.2s;
        padding: 0.7rem;
    }
    .stTextArea textarea:focus {
        border: 1.5px solid #0057B8;
        background: #f0f6ff;
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
    .result-card {
        background: #f8fbff;
        border-radius: 12px;
        box-shadow: 0 2px 8px #e3eafc;
        padding: 1.1rem 1.2rem 1.1rem 1.2rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid #0057B8;
        transition: box-shadow 0.2s;
    }
    .stDataFrame, .stJson {
        background: #f8fbff !important;
        border-radius: 10px;
        box-shadow: 0 2px 8px #e3eafc;
        padding: 0.5rem 0.5rem 0.5rem 0.5rem;
        margin-bottom: 1.2rem;
    }
    .stAlert, .stSuccess, .stWarning {
        border-radius: 8px !important;
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
<span class="rally-title">RALLY AI Response Evaluator Prompt Accuracy Tester</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown('<div class="section-header">1. Enter Your Data</div>', unsafe_allow_html=True)
user_golden_review = st.text_area("Golden Review", placeholder="Paste the golden review here...", height=100)
user_prompt = st.text_area("Prompt", placeholder="Paste your prompt here...", height=100)

llama_url = "http://localhost:11434/api/generate"
model = "llama3"
temperature = 0.2
top_k = 50
top_p = 0.9
num_predict = 200
file_path = "Response_Prompt_Testing.xlsx"

if 'llama_result' not in st.session_state:
    st.session_state['llama_result'] = None
if 'results' not in st.session_state:
    st.session_state['results'] = []

def call_llama(prompt_text, golden_review):
    full_prompt = f"{prompt_text}\n\nGOLDEN REVIEW:\n{golden_review}"
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "num_predict": num_predict
    }
    start_time = time.time()
    try:
        response = requests.post(llama_url, json=payload)
    except Exception as e:
        st.error(f"Llama request error: {e}")
        return '', '', '', ''
    end_time = time.time()
    if response.status_code == 200:
        data = response.json()
        reply = data.get('response', '')
        token_in = data.get('prompt_eval_count', '')
        token_out = data.get('eval_count', '')
        time_taken = round(end_time - start_time, 2)
        return reply.strip(), token_in, token_out, time_taken
    else:
        st.error(f"Llama API error: {response.text}")
        return '', '', '', ''

st.markdown('<div class="section-header">2. Run Evaluation</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if st.button("🚀 Run Llama Accuracy Test"):
    reply, token_in, token_out, time_taken = call_llama(user_prompt, user_golden_review)
    st.session_state['llama_result'] = {
        'Prompt': user_prompt,
        'Golden Review': user_golden_review,
        'Reply': reply,
        'Token In': token_in,
        'Token Out': token_out,
        'Time Taken (s)': time_taken
    }
    st.success("✅ Llama accuracy test complete!")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">3. Results</div>', unsafe_allow_html=True)

data = []

if st.session_state.get('llama_result'):
    st.markdown("""
        <div style="margin-bottom:0.5rem;">
            <span style="font-size:1.15rem;font-weight:700;color:#0057B8;">🦙 Llama (Original Prompt)</span>
        </div>
    """, unsafe_allow_html=True)
    with st.expander("📄 Show Original Prompt", expanded=False):
        st.code(st.session_state['llama_result']['Prompt'], language="markdown")
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.write("**Llama Reply:**")
    st.markdown(f"<div style='color:#444;font-size:1.08rem;background:#f7fafd;border-radius:8px;padding:0.7rem;margin-bottom:0.5rem;'>{st.session_state['llama_result']['Reply']}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    data.append(st.session_state['llama_result'])

# --- Save and Download ---
if len(data) == 1:
    df_new = pd.DataFrame(data)
    if os.path.exists(file_path):
        # Append new data to existing file
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            df_existing = pd.read_excel(file_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_excel(writer, index=False)
    else:
        df_new.to_excel(file_path, index=False)
        df_combined = df_new
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    for col in ws.columns:
        for cell in col:
            cell.alignment = openpyxl.styles.Alignment(wrap_text=True)
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                cell_length = len(str(cell.value)) if cell.value else 0
                if cell_length > max_length:
                    max_length = cell_length
            except:
                pass
        ws.column_dimensions[col_letter].width = min(max_length + 2, 60)
    wb.save(file_path)
    st.success("✅ Results saved to Excel!")

if len(data) >= 1:
    st.markdown("""
        <div style="margin-top:1.5rem;margin-bottom:0.5rem;">
            <span style="font-size:1.13rem;font-weight:700;color:#0057B8;">🗂️ Full Results Table</span>
        </div>
    """, unsafe_allow_html=True)
    df_display = pd.DataFrame(data)
    st.dataframe(df_display, use_container_width=True)
    summary_cols = ["Token In", "Token Out", "Time Taken (s)"]
    summary_df = df_display[summary_cols] if all(col in df_display.columns for col in summary_cols) else pd.DataFrame()
    if not summary_df.empty:
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    with open(file_path, 'rb') as f:
        st.download_button(
            label="⬇️ Download Excel file",
            data=f,
            file_name="Response_Prompt_Testing.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    &copy; 2024 RALLY AI &mdash; All rights reserved.<br>
    Powered by <b>RALLY AI</b>
</div>
""", unsafe_allow_html=True)
