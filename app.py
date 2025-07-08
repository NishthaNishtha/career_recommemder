import streamlit as st
from recommender import recommend_careers

st.title("🚀 AI-Powered Career Recommendation System")
skills = st.multiselect("Select your skills:", ["Python", "SQL", "Excel", "Power BI", "Prompt Engineering"])

if st.button("Recommend"):
    results = recommend_careers(skills)
    st.success(f"Recommended Career Paths: {', '.join(results)}")
