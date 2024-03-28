from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from crewai_tools import tool

@tool("calculate_ats_percentage")
def calculate_ats_percentage(resume: str, job_description: str) -> str:
    """This function calculates the similarity percentage between a resume and a job description."""
    vectorizer = CountVectorizer()

    count_matrix = vectorizer.fit_transform([resume, job_description])

    cosine_sim = cosine_similarity(count_matrix)
    ats_percentage = cosine_sim[0][1] * 100
    print(f"ATS Percentage: {ats_percentage}")

    if ats_percentage >= 70:
        return f"Very good! Your resume is well-aligned with the job description. ATS Percentage: {ats_percentage}"
    else:
        return f"Unfortunately, your resume is not aligned with the job description. ATS Percentage: {ats_percentage}"
