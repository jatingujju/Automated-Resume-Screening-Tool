import os
import re
from PyPDF2 import PdfReader
import docx

# -----------------------------
# DEBUG INFO
# -----------------------------
print("Current working directory:", os.getcwd())

if not os.path.exists("resumes"):
    print("❌ 'resumes' folder not found!")
    exit()

print("Files in resumes folder:", os.listdir("resumes"))

# -----------------------------
# TEXT CLEANING FUNCTION
# -----------------------------
def clean_text(text):
    text = text.lower()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Fix common merged words (important for PDFs)
    replacements = {
        "bachelorofarts": "bachelor of arts",
        "highschool": "high school",
        "videoediting": "video editing",
        "workexperience": "work experience",
        "machinelearning": "machine learning",
        "dataanalysis": "data analysis"
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# -----------------------------
# SKILL EXTRACTION
# -----------------------------
def extract_skills(text):
    skills_list = [
        "python", "sql", "machine learning", "excel",
        "data analysis", "pandas", "numpy", "communication",
        "video editing", "management", "deep learning",
        "power bi", "tableau"
    ]

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills

# -----------------------------
# PDF EXTRACTION
# -----------------------------
def extract_text_from_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# -----------------------------
# DOCX EXTRACTION
# -----------------------------
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

# -----------------------------
# GENERAL EXTRACTOR
# -----------------------------
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return ""

# -----------------------------
# MAIN PROGRAM
# -----------------------------
if __name__ == "__main__":

    files = os.listdir("resumes")

    if len(files) == 0:
        print("❌ No resumes found in 'resumes' folder")
        exit()

    # Automatically pick first resume
    file_path = os.path.join("resumes", files[0])

    print("\n📄 Reading file:", file_path)

    # Extract text
    raw_text = extract_text(file_path)

    # Clean text
    cleaned_text = clean_text(raw_text)

    # Extract skills
    skills = extract_skills(cleaned_text)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    print("\n📄 Cleaned Text Preview:\n")
    print(cleaned_text[:500])

    print("\n🎯 Extracted Skills:\n")
    print(skills)