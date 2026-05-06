# src/features.py

import sqlite3
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _safe_list(must_have_raw):
    """Handle 'a, b, c' or JSON list."""
    if isinstance(must_have_raw, str):
        # try JSON first
        try:
            val = json.loads(must_have_raw)
            if isinstance(val, list):
                return [s.strip().lower() for s in val]
        except Exception:
            pass
        # fallback: comma-separated
        return [s.strip().lower() for s in must_have_raw.split(",") if s.strip()]
    return [s.strip().lower() for s in (must_have_raw or [])]


def _tfidf_sim(a: str, b: str) -> float:
    """Lightweight semantic-ish similarity without torch."""
    if not a or not b:
        return 0.0
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf = vec.fit_transform([a, b])
    return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])


def jd_resume_features(db, job_id, candidate_id):
    con = sqlite3.connect(db)
    cur = con.cursor()

    jd = cur.execute(
        "SELECT jd_text, must_have FROM jobs WHERE id=?",
        (job_id,)
    ).fetchone()

    rs = cur.execute(
        "SELECT parsed_json FROM resumes WHERE candidate_id=?",
        (candidate_id,)
    ).fetchone()

    con.close()

    if not jd or not rs:
        return {}

    jd_text, must_have_raw = jd
    must_have = _safe_list(must_have_raw)

    parsed = json.loads(rs[0]) if rs[0] else {}

    # -----------------------------
    # "EMBEDDING" (TF-IDF fallback)
    # -----------------------------
    resume_text = " ".join(parsed.get("skills", [])) + " " + str(parsed.get("education", ""))
    sim = _tfidf_sim(jd_text, resume_text)  # 0..1

    # -----------------------------
    # MUST-HAVE SKILLS MATCH
    # -----------------------------
    skills = set(s.lower() for s in parsed.get("skills", []))
    hits = sum(1 for s in must_have if s in skills)

    # -----------------------------
    # EXPERIENCE
    # -----------------------------
    years = parsed.get("years_exp") or 0.0

    # -----------------------------
    # GAP PENALTY (no negatives)
    # -----------------------------
    gap_penalty = max(0.0, 0.1 * (len(must_have) - hits))

    return {
        "sim_embedding": sim,
        "rule_musthave_hits": hits,
        "rule_musthave_total": len(must_have),
        "years_exp": years,
        "gap_penalty": gap_penalty
    }