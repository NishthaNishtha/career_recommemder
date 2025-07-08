import streamlit as st

# --- Set up Streamlit page ---
st.set_page_config(page_title="AI Career Recommender", layout="centered")
st.title("🚀 AI-Powered Career Recommendation System")

# Download NLTK stopwords before importing pyresparser
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Download and load SpaCy model before importing pyresparser
try:
    import spacy
    spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    import spacy

# NOW safely import ResumeParser AFTER required downloads
from pyresparser import ResumeParser

# Also import recommender functions (if available)
try:
    from recommender import recommend_careers, gpt_recommend_careers
except:
    def recommend_careers(skills):
        return ["Data Analyst", "AI Engineer"]

    def gpt_recommend_careers(skills):
        return "Based on your skills, you can explore roles like AI Specialist or Business Analyst."

# --- Skill-Based Recommendation ---
st.header("🎯 Select Your Skills")
skills = st.multiselect("Choose your skills:", ["Python", "SQL", "Excel", "Power BI", "Prompt Engineering"])

if st.button("🔍 Recommend Career Paths"):
    if skills:
        results = recommend_careers(skills)
        st.success(f"🔎 Suggested Careers: {', '.join(results)}")
    else:
        st.warning("Please select at least one skill.")

if st.button("🔮 GPT Career Suggestion"):
    if skills:
        response = gpt_recommend_careers(skills)
        st.info(response)
    else:
        st.warning("Please select at least one skill.")

# --- Resume Upload and Parsing ---
st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
if uploaded_file is not None:
    file_path = "uploaded_resume." + uploaded_file.name.split('.')[-1]
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        parsed_data = ResumeParser(file_path).get_extracted_data()
        extracted_skills = parsed_data.get("skills", [])
        st.success(f"✅ Extracted Skills: {', '.join(extracted_skills)}")

        if st.button("💡 GPT Suggestion From Resume"):
            if extracted_skills:
                response = gpt_recommend_careers(extracted_skills)
                st.info(response)
            else:
                st.warning("No skills were extracted from your resume.")
    except Exception as e:
        st.error("❌ Could not parse your resume. Please upload a proper PDF/DOCX format.")
        st.exception(e)
