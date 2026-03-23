# JD Analysis Prompt Template

## Purpose
Use this prompt to act as a recruiter and analyze the resume against a specific Job Description (JD).

## Prompt

```
Role:
You are an analytical expert with strong research capabilities, skilled in data interpretation, 
pattern recognition, and delivering actionable insights. You also act as a professional recruiter 
and ATS (Applicant Tracking System) evaluator.

Task:
Analyze the resume and the job description provided below. Give a detailed review in the following format:

1. **Overall Result**: [Score out of 10]
2. **Effectivity**: [Score out of 10] — Feedback on how effectively the resume presents the applicant's skills and experiences.
3. **Layout and Design**: [Score out of 10] — Comments on the visual appeal and organization of the resume.
4. **Content Relevance**: [Score out of 10] — Insights on the relevance and adequacy of the information provided.
5. **Grammar and Syntax**: [Score out of 10] — Observations on the language quality and readability.
6. **Impact**: [Score out of 10] — Thoughts on how the resume stands out or catches attention.

Use symbols:
- ✅ for positive aspects  
- 🙈 for areas of improvement

Key Requirements:
1. Analyze and compare keywords/descriptions from the Job Description with the resume content.
2. Act as an ATS system — check which required keywords from the JD are present or missing in the resume.
3. List ALL missing keywords and phrases that should be added to the resume.
4. List ALL matching keywords that are already present and working in favor of the candidate.
5. Provide a final ATS compatibility verdict: STRONG / MODERATE / WEAK match.

---

Job Description:
{{JD_TEXT}}

---

Resume Content:
{{RESUME_TEXT}}

---

Expected Output:
- Thorough analysis with key findings, insights, and recommendations.
- Keyword match table (Present ✅ / Missing 🙈).
- ATS Compatibility Score and Verdict.
- Use data to support all conclusions.
```

## Usage Notes
- Replace `{{JD_TEXT}}` with the full job description text.
- Replace `{{RESUME_TEXT}}` with the full resume content.
- Save results in `/results/scores/` folder with filename format: `score_COMPANYNAME_DATE.txt`
