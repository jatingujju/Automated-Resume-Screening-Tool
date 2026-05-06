import json
import sqlite3
import datetime as dt

from src.features import jd_resume_features


def _parse_must_have(raw):
    if isinstance(raw, str):
        # handle "a, b, c"
        return [s.strip().lower() for s in raw.split(",") if s.strip()]
    return raw or []


def ensure_rankings_table(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rankings (
            job_id TEXT,
            candidate_id TEXT,
            score REAL,
            reasons TEXT,
            created_at TEXT,
            PRIMARY KEY (job_id, candidate_id)
        )
    """)
    con.commit()
    con.close()


def rank_job(db, job_id, min_req_years=2.0):
    ensure_rankings_table(db)

    con = sqlite3.connect(db)
    cur = con.cursor()

    # get candidates
    cands = cur.execute("SELECT candidate_id FROM resumes").fetchall()

    # get job info
    job = cur.execute(
        "SELECT must_have, min_exp_years FROM jobs WHERE id=?",
        (job_id,)
    ).fetchone()

    if not job:
        print("❌ Job not found")
        con.close()
        return

    must_have = _parse_must_have(job[0])
    must_total = len(must_have)
    min_req = job[1] if job[1] else min_req_years

    rows = []

    print(f"\n🚀 Ranking {len(cands)} candidates...\n")

    for (cid,) in cands:
        f = jd_resume_features(db, job_id, cid)
        if not f:
            continue

        # ---- scoring (same idea as your main)
        skill_ratio = f["rule_musthave_hits"] / max(1, must_total)
        exp_score = min(1.0, (f["years_exp"] or 0.0) / min_req)

        score = (
            0.5 * f["sim_embedding"] +
            0.3 * skill_ratio +
            0.2 * exp_score
        )

        # ---- reasons (key part)
        reasons = {
            "skills_match": f"{f['rule_musthave_hits']}/{must_total}",
            "similarity": round(f["sim_embedding"], 3),
            "experience_ok": (f["years_exp"] or 0.0) >= min_req
        }

        print(f"Candidate: {cid[:8]} | Score: {round(score*100,2)}%")

        rows.append((
            job_id,
            cid,
            float(score),
            json.dumps(reasons),
            dt.datetime.utcnow().isoformat()
        ))

    # save to DB
    cur.executemany("""
        INSERT OR REPLACE INTO rankings
        (job_id, candidate_id, score, reasons, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, rows)

    con.commit()
    con.close()

    print("\n✅ Rankings stored in DB!")