import streamlit as st
import os
import tempfile
# from rag_engine import process_resume_and_roast  # Uncomment when rag_engine is available
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------
# 1. Page Configuration
# -----------------------------------------
st.set_page_config(
    page_title="RoastMyResume — Brutal Honesty, Free of Charge",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------
# 2. Global CSS — Dark editorial + fire theme
# -----------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0c0c0c !important;
    color: #e8e0d4 !important;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(255, 80, 20, 0.18) 0%, transparent 70%),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 39px,
            rgba(255,255,255,0.02) 39px,
            rgba(255,255,255,0.02) 40px
        );
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"] { display: none; }
footer { display: none !important; }
.block-container { padding-top: 2.5rem !important; max-width: 780px !important; }

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 3rem 0 1.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff5014;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 12vw, 6.5rem);
    line-height: 0.92;
    letter-spacing: 0.02em;
    color: #fff;
    margin: 0;
    text-shadow: 0 0 80px rgba(255, 80, 20, 0.45);
}
.hero-title span {
    color: #ff5014;
    display: inline-block;
    animation: flicker 4s infinite;
}
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 1.05rem;
    color: #7a7060;
    margin-top: 1rem;
    letter-spacing: 0.02em;
}

@keyframes flicker {
    0%,19%,21%,23%,25%,54%,56%,100% { opacity: 1; text-shadow: 0 0 80px rgba(255,80,20,0.6); }
    20%,22%,24%,55% { opacity: 0.85; text-shadow: none; }
}

/* ── Divider ── */
.flame-divider {
    text-align: center;
    font-size: 1.3rem;
    letter-spacing: 0.6em;
    margin: 0.5rem 0 2rem;
    color: #3a2a1a;
}

/* ── Upload card ── */
.upload-card {
    background: #141414;
    border: 1px solid #2a2218;
    border-radius: 4px;
    padding: 1.6rem 1.8rem 1.2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.upload-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #ff5014, #ff9500, #ff5014);
    background-size: 200% 100%;
    animation: shimmer 2.5s infinite linear;
}
@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.card-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #ff5014;
    margin-bottom: 0.8rem;
    display: block;
}

/* ── File uploader overrides ── */
[data-testid="stFileUploader"] {
    background: #0e0e0e !important;
    border: 1px dashed #2e2418 !important;
    border-radius: 4px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #ff5014 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p {
    color: #4a4030 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
}
[data-testid="stFileUploaderDropzone"] svg { color: #ff5014 !important; }

/* ── Text area overrides ── */
textarea {
    background: #0e0e0e !important;
    border: 1px solid #2a2218 !important;
    border-radius: 4px !important;
    color: #c8b89a !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    caret-color: #ff5014 !important;
    resize: none !important;
}
textarea:focus {
    border-color: #ff5014 !important;
    box-shadow: 0 0 0 2px rgba(255,80,20,0.15) !important;
}
textarea::placeholder { color: #3a2e22 !important; }

/* ── Label overrides ── */
label[data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #6a5a48 !important;
}

/* ── CTA Button ── */
.stButton > button {
    width: 100% !important;
    background: #ff5014 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.6rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.85rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 30px rgba(255, 80, 20, 0.3) !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: #e03e00 !important;
    box-shadow: 0 6px 40px rgba(255, 80, 20, 0.55) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Status / Spinner ── */
[data-testid="stStatusWidget"] {
    background: #141414 !important;
    border: 1px solid #2a2218 !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    color: #c8b89a !important;
    font-size: 0.8rem !important;
}

/* ── Result box ── */
.result-container {
    background: #101010;
    border: 1px solid #2a2218;
    border-left: 3px solid #ff5014;
    border-radius: 4px;
    padding: 2rem 2.2rem;
    margin-top: 1.5rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    line-height: 1.75;
    color: #d4c8b8;
}
.result-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.1em;
    color: #ff5014;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: #1a0f0a !important;
    border: 1px solid #ff5014 !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #ff8060 !important;
}

/* ── Footer tag ── */
.footer-tag {
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    color: #2a2218;
    text-transform: uppercase;
    margin-top: 3rem;
    padding-bottom: 2rem;
}

/* ── Stat bar ── */
.stat-bar {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin: 1.5rem 0 2rem;
    padding: 1rem 0;
    border-top: 1px solid #1c1c1c;
    border-bottom: 1px solid #1c1c1c;
}
.stat-item {
    text-align: center;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: #ff5014;
    display: block;
    line-height: 1;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3a3028;
    display: block;
    margin-top: 0.3rem;
}

/* ── Success override ── */
.stSuccess {
    display: none !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: transparent !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# 3. Hero Section
# -----------------------------------------
st.markdown("""
<div class="hero-wrap">
    <p class="hero-eyebrow">⚡ Powered by Llama 3.1 + RAG</p>
    <h1 class="hero-title">Roast<span>My</span>Resume</h1>
    <p class="hero-subtitle">Upload your resume. Brace yourself. Get hired — or cry trying.</p>
</div>
<div class="flame-divider">Don't take it personally</div>
""", unsafe_allow_html=True)

# Fake social-proof stats
st.markdown("""
<div class="stat-bar">
    <div class="stat-item">
        <span class="stat-value">4,217</span>
        <span class="stat-label">Resumes Roasted</span>
    </div>
    <div class="stat-item">
        <span class="stat-value">91%</span>
        <span class="stat-label">Said it stung</span>
    </div>
    <div class="stat-item">
        <span class="stat-value">0</span>
        <span class="stat-label">Feelings Spared</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------
# 4. Input Cards
# -----------------------------------------
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<span class="card-label">📄 Step 1 — Your Resume</span>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your PDF here",
    type="pdf",
    help="PDF only. Max 10MB. We won't save it.",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<span class="card-label">🎯 Step 2 — Target Job (Optional but recommended)</span>', unsafe_allow_html=True)
job_desc = st.text_area(
    "Job description",
    height=110,
    placeholder="Paste the job description here...\ne.g. Senior AI Engineer, 5+ yrs Python, LLMs, distributed systems...",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# 5. CTA Button + Logic
# -----------------------------------------
roast_clicked = st.button("🔥 ROAST MY RESUME — I'M READY")

if roast_clicked:
    if not uploaded_file:
        st.error("🚨 You forgot to attach your resume. We can't roast thin air.")
    else:
        with st.status("Initializing the roast...", expanded=True) as status:
            st.write("🕵️‍♂️ Extracting your life choices from PDF...")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                temp_filepath = tmp.name

            st.write("🧠 Warming up Llama 3.1...")
            st.write("🔎 Running RAG retrieval pipeline...")
            st.write("💀 Preparing brutal-but-constructive feedback...")

            try:
                target_jd = job_desc.strip() if job_desc.strip() else "General Software Engineering Role"

                # ── Replace with your actual call ──
                # roast_result = process_resume_and_roast(temp_filepath, target_jd)

                # Demo placeholder (remove when integrating)
                roast_result = """
**Overall Verdict:** Your resume has the energy of a LinkedIn post written at 2am after watching a motivational YouTube video.

**What's working:**
- You've got relevant experience — it's just buried under 11 bullet points that all start with "Responsible for..."
- The skills section is comprehensive, but listing "Microsoft Word" in 2024 is a choice.

**What needs fixing:**
1. **Quantify everything.** "Improved performance" means nothing. By how much? Over what timeframe?
2. **Your summary reads like it was written by a ChatGPT prompt.** "Passionate, results-driven professional with a proven track record" — who wrote this, your elevator?
3. **Two-page resume for 2 years of experience?** Bold. Audacious. Wrong.
4. **The font is Calibri.** Helvetica called. It's not even mad. It's just disappointed.

**For this specific role:** You're missing 4 of the 6 key requirements in the JD. Lead with what they asked for, not your college GPA from 2019.

**Bottom line:** Fix the bullets, cut a page, and stop listing hobbies unless you're applying to a podcast. You're closer than you think — but this version is getting auto-rejected at resume screen.
                """

                status.update(label="Roast complete. Grab some ice. ❄️", state="complete", expanded=False)
                st.balloons()

                # Result display
                st.markdown(f"""
                <div class="result-container">
                    <div class="result-header">💀 Your Roast Report</div>
                    {roast_result.strip().replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                status.update(label="Something caught fire (not in a good way).", state="error")
                st.error(f"Error: {str(e)}")
            finally:
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)

# -----------------------------------------
# 6. Footer
# -----------------------------------------
st.markdown("""
<div class="footer-tag">
    RoastMyResume · Built with Llama 3.1 + RAG · No resumes stored · No feelings guaranteed
</div>
""", unsafe_allow_html=True)