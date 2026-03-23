# Cover Letter Prompt Template

## Purpose
Use this prompt to generate a professional, tailored cover letter based on a Job Description and your resume.

## Prompt

```
Role:
You are an expert professional writer specializing in career documents, with deep knowledge 
of hiring practices, company culture research, and persuasive writing.

Task:
Write a compelling cover letter for a job application using the details provided below.

Analyze both the Job Description and the Resume thoroughly, then craft a cover letter that:

1. **Opens** with a professional greeting addressed to the hiring manager (use "Dear Hiring Manager" 
   if name is unknown).

2. **Introduction Paragraph**: 
   - Introduce the candidate by name.
   - State the exact position they are applying for.
   - Express genuine interest in both the role and the company.

3. **Experience & Skills Paragraph**:
   - Elaborate on how previous work experience and specific skills make them the ideal candidate.
   - Draw direct connections between the candidate's background and the JD requirements.
   - Use specific, quantifiable examples wherever possible.

4. **Achievements Paragraph**:
   - Highlight 1-2 significant career achievements that are directly relevant to the job.
   - Frame achievements using impact-driven language (results, metrics, outcomes).

5. **Company Alignment Paragraph**:
   - Discuss how the candidate aligns with the company's values, mission, or culture.
   - Show that the candidate has researched the company.

6. **Closing**:
   - Strong closing statement expressing eagerness for an interview.
   - Thank the reader for their time and consideration.
   - Professional sign-off.

Formatting Rules:
- Maximum ONE page in length.
- Professional, confident, and engaging tone.
- Tailored specifically to the JD — avoid generic language.
- No buzzwords or clichés (e.g., avoid: "team player", "hard worker", "passionate").

---

Job Description:
{{JD_TEXT}}

---

Resume Details:
{{RESUME_TEXT}}

---

Candidate Name: {{CANDIDATE_NAME}}
Position Applying For: {{POSITION}}
Company Name: {{COMPANY_NAME}}
```

## Usage Notes
- Replace all `{{PLACEHOLDERS}}` before sending to LLM.
- Save cover letters in `/results/cover-letters/` with format: `coverletter_COMPANYNAME_DATE.docx`
- Always review the cover letter for accuracy before submitting.
