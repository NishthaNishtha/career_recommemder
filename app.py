import streamlit as st

st.set_page_config(page_title="AI Career Recommender", layout="centered")
st.title("🚀 AI-Powered Career Recommendation System")
#####
import nltk
nltk.download('stopwords')  # download BEFORE pyresparser is used

import spacy
try:
    spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")

from pyresparser import ResumeParser  # moved AFTER nltk setup
import os


#####
from recommender import recommend_careers

st.title("🚀 AI-Powered Career Recommendation System")
skills = st.multiselect("Select your skills:", ["Python", "SQL", "Excel", "Power BI", "Prompt Engineering"])

if st.button("Recommend"):
    results = recommend_careers(skills)
    st.success(f"Recommended Career Paths: {', '.join(results)}")

#for resume
import os
from pyresparser import ResumeParser

st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
if uploaded_file is not None:
    with open("uploaded_resume." + uploaded_file.name.split('.')[-1], "wb") as f:
        f.write(uploaded_file.read())

    parsed_data = ResumeParser("uploaded_resume." + uploaded_file.name.split('.')[-1]).get_extracted_data()
    extracted_skills = parsed_data.get("skills", [])
    st.success(f"✅ Extracted Skills: {', '.join(extracted_skills)}")

    if st.button("🔮 GPT Based Recommendation (From Resume)"):
        response = gpt_recommend_careers(extracted_skills)
        st.info(response)
