def recommend_careers(user_skills):
    mapping = {
        "Python": "Data Scientist",
        "SQL": "Data Analyst",
        "Excel": "Business Analyst",
        "Power BI": "BI Developer",
        "Prompt Engineering": "AI Specialist"
    }
    careers = set()
    for skill in user_skills:
        if skill in mapping:
            careers.add(mapping[skill])
    return list(careers)
