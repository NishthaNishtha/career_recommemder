import streamlit as st
import nltk
import os

# Setup Streamlit page
st.set_page_config(page_title="AI Career Recommender", layout="centered")
st.title("🚀 AI-Powered Career Recommendation System")

# Ensure required NLTK + SpaCy models are downloaded
nltk.download('stopwords')

try:
    import spacy
    spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    import spacy

from pyresparser import ResumeParser
from recommender import recommend_careers, gpt_recommend_careers

# Section: Manual Skill Selection
st.header("🎯 Select Your Skills")
skills = st.multiselect("Choose your skills:", ["Python", "SQL", "Excel", "Power BI", "Prompt Engineering"])

if st.button("Recommend Career Paths"):
    if skills:
        results = recommend_careers(skills)
        st.success(f"🔎 Suggested Careers: {', '.join(results)}")
    else:
        st.warning("Please select at least one skill.")

if st.button("🔮 GPT-Powered Suggestions"):
    if skills:
        response = gpt_recommend_careers(skills)
        st.info(response)
    else:
        st.warning("Please select at least one skill.")

# Section: Resume Upload
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

        if st.button("💡 GPT Suggestion Based on Resume"):
            if extracted_skills:
                response = gpt_recommend_careers(extracted_skills)
                st.info(response)
            else:
                st.warning("No skills were extracted from your resume.")
    except Exception as e:
        st.error("❌ Failed to parse the resume. Make sure it's a proper format and retry.")
        st.exception(e)
