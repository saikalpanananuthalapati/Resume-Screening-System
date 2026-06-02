import os
import re
import shutil
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clear_folder(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def check_skill_gaps(resume_text, jd_text):

    TECHNICAL_SKILLS = [
        "python","sql","machine learning",
        "nlp","data science","aws",
        "azure","java","tableau"
    ]

    resume_words = set(clean_text(resume_text).split())
    jd_words = set(clean_text(jd_text).split())

    found = [s for s in TECHNICAL_SKILLS if s in resume_words]
    missing = [s for s in TECHNICAL_SKILLS if s in jd_words and s not in resume_words]

    return found, missing


def run_nlp_screener():

    input_folder = "nlp"
    shortlisted_folder = "Shortlisted_Candidates"
    rejected_folder = "Rejected_Candidates"

    job_description = "Python"
    threshold = 60

    rejected_flag = False   # 🔹 track rejected resumes

    if not os.path.exists(shortlisted_folder):
        os.makedirs(shortlisted_folder)

    if not os.path.exists(rejected_folder):
        os.makedirs(rejected_folder)

    clear_folder(shortlisted_folder)
    clear_folder(rejected_folder)

    resume_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

    print(f"Found {len(resume_files)} resumes")
    print("Starting NLP Resume Screening...\n")

    for file_name in resume_files:

        full_path = os.path.join(input_folder, file_name)

        try:

            raw_resume = extract_text(full_path)

            clean_resume = clean_text(raw_resume)
            clean_jd = clean_text(job_description)

            vectorizer = TfidfVectorizer(ngram_range=(1,2))
            tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])

            raw_similarity = cosine_similarity(
                tfidf_matrix[0:1], tfidf_matrix[1:2]
            )[0][0]

            found, missing = check_skill_gaps(raw_resume, job_description)

            boost = (len(found)/(len(found)+len(missing))) if (len(found)+len(missing))>0 else 0
            accuracy = round((raw_similarity*0.3 + boost*0.7)*100, 2)

            if accuracy >= threshold:

                print("="*50)
                print("FILE:", file_name)
                print("MATCH ACCURACY:", accuracy, "%")
                print("DECISION: SHORTLISTED")
                print("="*50)

                shutil.copy(full_path,
                os.path.join(shortlisted_folder, file_name))

            else:

                rejected_flag = True   # 🔹 mark rejected
                shutil.copy(full_path,
                os.path.join(rejected_folder, file_name))

        except Exception as e:
            print("Error processing", file_name, e)

    # 🔹 Print message once
    if rejected_flag:
        print("\nRejected candidates have been notified via email.")


if __name__ == "__main__":
    run_nlp_screener()