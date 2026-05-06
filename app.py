from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
import sqlite3
import uuid
import json
import os

from src.extract import parse_resume
from src.rank import rank_job

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = "data/resume.db"


# -----------------------------
# JOB MODEL
# -----------------------------
class Job(BaseModel):
    title: str
    jd_text: str
    must_have: list[str] = []
    nice_to_have: list[str] = []
    min_exp_years: float = 2.0
    location: str | None = None


# -----------------------------
# CREATE JOB
# -----------------------------
@app.post("/job/create")
def job_create(j: Job):
    jid = str(uuid.uuid4())

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs (id, title, jd_text, must_have, nice_to_have, min_exp_years, location)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        jid,
        j.title,
        j.jd_text,
        json.dumps(j.must_have),
        json.dumps(j.nice_to_have),
        j.min_exp_years,
        j.location
    ))

    conn.commit()
    conn.close()

    return {"job_id": jid}


# -----------------------------
# UPLOAD RESUME
# -----------------------------
@app.post("/resume/upload")
async def resume_upload(candidate_id: str = Form(...), file: UploadFile = Form(...)):

    content = await file.read()

    # handle txt / pdf / docx simply
    try:
        raw = content.decode("utf-8", errors="ignore")
    except:
        raw = ""

    parsed = parse_resume(raw)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO resumes (candidate_id, source, raw_text, parsed_json)
        VALUES (?, ?, ?, ?)
    """, (
        candidate_id,
        file.filename,
        raw,
        json.dumps(parsed)
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Resume uploaded",
        "skills": parsed.get("skills", [])
    }


# -----------------------------
# RANK CANDIDATES
# -----------------------------
@app.post("/rank/{job_id}")
def rank(job_id: str):

    # run ranking logic
    rank_job(DB, job_id)

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT candidate_id, score, reasons
        FROM rankings
        WHERE job_id=?
        ORDER BY score DESC
        LIMIT 20
    """, (job_id,)).fetchall()

    conn.close()

    return [dict(r) for r in rows]