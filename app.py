import streamlit as st
import os
import tempfile
from rag_engine import process_resume_and_roast
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------
# 1. Page Configuration & Custom CSS
# -----------------------------------------
st.set_page_config(
    page_title="RoastMyResume | AI Brutal Honesty", 
    page_icon="🔥", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to make it look less like a default Streamlit app
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF0000;
        transform: scale(1.02);
    }
    .main-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #888;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# 2. UI Layout
# -----------------------------------------
st.markdown("<div class='main-header'>🔥 RoastMyResume</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Upload your resume. Brace yourself. Get hired.</div>", unsafe_allow_html=True)

# Use columns for a cleaner upload section
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf", help="Max size: 10MB")

with col2:
    # Use an expander for the job description to keep the UI clean
    with st.expander("🎯 Target Job Description (Optional but recommended)", expanded=True):
        job_desc = st.text_area(
            "Paste the JD here:", 
            height=130, 
            placeholder="e.g. Looking for a Senior AI Engineer with 5+ years of Python..."
        )

st.markdown("---")

# -----------------------------------------
# 3. Execution & State Handling
# -----------------------------------------
if st.button("ROAST ME 💀", type="primary"):
    if not uploaded_file:
        st.error("🚨 We can't roast nothing. Upload a PDF first.")
    else:
        # Fun UI loading states
        with st.status("Analyzing your life choices...", expanded=True) as status:
            st.write("🕵️‍♂️ Scanning document...")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_filepath = temp_file.name
                
            st.write("🧠 Firing up the Llama 3.1 LLM...")
            
            try:
                # If they didn't provide a JD, pass a default string
                target_jd = job_desc if job_desc else "General Software Engineering Role"
                
                # Call the backend RAG engine
                roast_result = process_resume_and_roast(temp_filepath, target_jd)
                
                status.update(label="Analysis Complete! Prepare to cry.", state="complete", expanded=False)
                
                # Show balloons for a fun UX finish
                st.balloons()
                
                # Display the results inside a nice container
                with st.container():
                    st.success("Here is your brutal feedback:")
                    st.markdown(roast_result)
                    
            except Exception as e:
                status.update(label="Something broke.", state="error")
                st.error(f"Error details: {str(e)}")
            finally:
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)