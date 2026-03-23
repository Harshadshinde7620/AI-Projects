# AI Job Assistant — Harshad Shinde

An AI-powered personal career tool to score, tailor, and submit job-ready resumes and cover letters.

---

## 📁 Folder Structure

```
job-assistant-ai/
│
├── templates/
│   ├── ats_score_prompt.md
│   ├── jd_analysis_prompt.md
│   ├── resume_update_prompt.md
│   └── cover_letter_prompt.md
│
├── resumes/              ← PUT YOUR MASTER RESUME HERE (.pdf / .docx)
├── job-descriptions/     ← PASTE JD TEXT FILES HERE (.txt)
│
├── results/
│   ├── scores/           ← ATS scores & JD analysis (.txt)
│   ├── updated-resumes/  ← Tailored PDFs (max 2 pages)
│   └── cover-letters/    ← Generated cover letters (PDF)
│
├── scripts/
│   └── job_assistant.py  ← Main script — run this!
│
├── requirements.txt
└── README.md
```

---

## 📄 Resume Naming Convention

Every updated resume is saved as:

```
Harshad Shinde_QA_resume_[COMPANY_INITIALS].pdf
```

Examples:
| Company            | File Saved As                         |
|--------------------|---------------------------------------|
| Physics Wala       | Harshad Shinde_QA_resume_PW.pdf       |
| Tata Consultancy   | Harshad Shinde_QA_resume_TC.pdf       |
| Google             | Harshad Shinde_QA_resume_G.pdf        |
| Infosys            | Harshad Shinde_QA_resume_I.pdf        |

Initials are auto-detected from the company name you enter — no manual input needed.

---

## ⚠️ 2-Page Rule

All updated resumes are STRICTLY capped at 2 pages (A4), enforced two ways:
1. AI Prompt — instructs Claude to keep Summary to 3-4 lines, 4-5 bullets per job, inline skills.
2. PDF Builder — if the first render exceeds 2 pages, fonts are reduced automatically and rebuilt.

---

## ⚡ Quick Start

Step 1 — Install:
  pip install -r requirements.txt

Step 2 — Add files:
  Drop resume (PDF/DOCX) into /resumes/
  Paste JD text into /job-descriptions/jd_company.txt

Step 3 — Run:
  cd scripts
  python job_assistant.py

---

## 🔑 API Key

  Windows : set ANTHROPIC_API_KEY=your_key_here
  Mac/Linux: export ANTHROPIC_API_KEY=your_key_here

Or enter it when prompted on launch.

---

## 📋 Menu Options

  1. ATS Score Only      → ats_score_[INITIALS]_DATE.txt
  2. JD Analysis         → jd_analysis_[INITIALS]_DATE.txt
  3. Update Resume (PDF) → Harshad Shinde_QA_resume_[INITIALS].pdf
  4. Cover Letter (PDF)  → Harshad Shinde_CoverLetter_[INITIALS]_DATE.pdf
  5. Full Pipeline       → All three outputs at once (recommended)

---

## 🛠 Troubleshooting

  anthropic not found  → pip install anthropic
  PyPDF2 not found     → pip install PyPDF2
  python-docx missing  → pip install python-docx
  reportlab missing    → pip install reportlab
  Resume > 2 pages     → Script auto-shrinks and rebuilds (no action needed)

---

Personal AI Career Assistant — built for Harshad Shinde.