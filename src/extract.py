# src/extract.py

import re

# -----------------------------
# SKILLS LIST
# -----------------------------
SKILLS = [
    "communication",
    "video editing",
    "content creation",
    "teamwork",
    "leadership",
    "social media",
    "creativity",
    "time management",
    "digital marketing",
    "video production"
]

# -----------------------------
# SKILL EXTRACTION
# -----------------------------
def extract_skills(text: str):
    text = text.lower()
    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return sorted(list(set(found)))


# -----------------------------
# EXPERIENCE EXTRACTION
# -----------------------------
def total_years(text: str):
    matches = re.findall(r'(\d+)\s*(years|yrs|y)', text.lower())
    return int(matches[0][0]) if matches else None


# -----------------------------
# EDUCATION EXTRACTION
# -----------------------------
def extract_education(text: str):
    text = text.lower()

    if "bachelor" in text:
        return "Bachelor"
    elif "master" in text:
        return "Master"

    return None


# -----------------------------
# MAIN PARSER
# -----------------------------
def parse_resume(raw: str):
    return {
        "skills": extract_skills(raw),
        "years_exp": total_years(raw),
        "education": extract_education(raw)
    }