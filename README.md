# 🚀 Automated Resume Screening ToolAn AI-powered Automated Resume Screening System built using Python, NLP, FastAPI, and Next.js.This project helps recruiters automatically analyze resumes, extract skills, compare candidates with job descriptions, and rank applicants using TF-IDF and cosine similarity scoring.---# 📌
Features
✅ Resume PDF text extraction 
✅ DOCX resume extraction  
✅ Job description matching 
✅ Text cleaning & preprocessing 
✅ Keyword / skill extraction  
✅ TF-IDF vectorization  
✅ Cosine similarity scoring 
✅ Resume ranking system 
✅ Candidate shortlist decision
✅ CSV report generation 
✅ FastAPI backend  
✅ Next.js frontend dashboard
✅ Recruiter ranking interface  ---# 🧠 Tech Stack## Backend- Python- FastAPI- SQLite## NLP / ML- Scikit-learn- TF-IDF Vectorizer- Cosine Similarity- Sentence Transformers## Frontend- Next.js- React- Tailwind CSS---# 📁 Project Structure```textAutomated-Resume-Screening-Tool/│├── data/├── outputs/├── resumes/├── src/│├── app.py├── main.py├── evaluate.py├── ingestion.py├── README.md

⚙️ Installation
Clone Repository
git clone https://github.com/jatingujju/Automated-Resume-Screening-Tool.git

Move into Project Folder
cd Automated-Resume-Screening-Tool

Install Dependencies
pip install -r requirements.txt

▶️ Run Backend
uvicorn app:app --reload
Backend runs at:
http://127.0.0.1:8000

▶️ Run Frontend
Move to frontend folder:
cd resume-ui
Install packages:
npm install
Run frontend:
npm run dev
Frontend runs at:
http://localhost:3000

📊 ATS Scoring Logic
The system combines:


semantic similarity


skill matching


experience validation


Final score formula:
Final Score =0.55 × embedding similarity+ 0.35 × must-have skill coverage+ 0.10 × experience score- gap penalty

⚡ Latency Targets
ComponentTargetResume Parsing< 2 secEmbedding Generation< 1 secCandidate Ranking< 500 msAPI Response< 1 sec

🔒 Privacy & Bias Safeguards
Privacy


Secure resume storage


Limited sensitive data retention


File validation for uploads


Local processing support


Bias Mitigation


Skill-focused ranking


Ignore demographic attributes


Human recruiter review


Bias-aware evaluation strategy



🔄 Human Feedback Retraining Loop
Recruiter Review       ↓Accept / Reject Candidates       ↓Store Feedback       ↓Update Training Data       ↓Retrain Ranking Model       ↓Improve Future Recommendations

📈 Evaluation Metrics
The project supports:


ROC-AUC


Precision@K


Recall


F1-score


Top-K candidate ranking evaluation



🎯 Future Improvements


Resume upload UI


Authentication system


Recruiter dashboard analytics


Real-time resume parsing


Vector database integration


LLM-powered candidate explanations


Cloud deployment



👨‍💻 Author
Jatin Gujarathi
GitHub:
https://github.com/jatingujju

⭐ If you like this project
Give it a star on GitHub ⭐
