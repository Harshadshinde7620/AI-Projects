"""
linkedin_agent.py
==================
Automates LinkedIn job search and Easy Apply.

Flow:
  1. Login (session cached — only asks for password once)
  2. Search jobs using preferences from job_preferences.json
  3. Extract JD text from each listing
  4. Score JD against master resume (via Claude)
  5. If score >= threshold → generate tailored resume + cover letter
  6. Apply via LinkedIn Easy Apply (fills form fields automatically)
  7. Log result to results/applied_jobs/
"""

import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from agents.browser_base import launch_browser, close_browser, human_delay, human_type

# Load credentials from .env
load_dotenv(Path(__file__).parent.parent / "credentials" / ".env")

BASE_DIR    = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "job_preferences.json"
LOG_DIR     = BASE_DIR / "results" / "applied_jobs"
JD_DIR      = BASE_DIR / "results" / "jd_extracted"
LOG_DIR.mkdir(parents=True, exist_ok=True)
JD_DIR.mkdir(parents=True, exist_ok=True)

LINKEDIN_URL = "https://www.linkedin.com"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


# ─── Step 1: Login ────────────────────────────────────────────────────────────
async def linkedin_login(page) -> bool:
    """
    Login to LinkedIn. If session is already saved, this is skipped automatically.
    Returns True if logged in successfully.
    """
    await page.goto(f"{LINKEDIN_URL}/feed", wait_until="domcontentloaded")
    await human_delay(1500, 2500)

    # Check if already logged in
    if "/feed" in page.url or "/jobs" in page.url:
        print("  Already logged in to LinkedIn (session active).")
        return True

    print("  Logging in to LinkedIn...")
    await page.goto(f"{LINKEDIN_URL}/login", wait_until="domcontentloaded")
    await human_delay(1000, 1800)

    email    = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    await human_type(page, "#username", email)
    await human_delay(400, 900)
    await human_type(page, "#password", password)
    await human_delay(600, 1200)
    await page.click('button[type="submit"]')
    await human_delay(3000, 5000)

    if "/feed" in page.url or "/jobs" in page.url:
        print("  LinkedIn login successful.")
        return True
    else:
        print("  LinkedIn login may require 2FA or CAPTCHA.")
        print("  Please complete it manually in the browser window, then press Enter here.")
        input("  [Press Enter after completing manual verification] > ")
        return True


# ─── Step 2: Search Jobs ──────────────────────────────────────────────────────
async def search_linkedin_jobs(page, config: dict) -> list:
    """
    Search LinkedIn jobs based on job_preferences.json.
    Returns a list of job dicts: {title, company, location, url, jd_text}
    """
    prefs    = config["search"]
    results  = []
    max_jobs = prefs.get("max_jobs_per_run", 10)

    for job_title in prefs["job_titles"]:
        if len(results) >= max_jobs:
            break

        location = prefs["locations"][0]  # Primary location
        print(f"\n  Searching: '{job_title}' in '{location}' ...")

        # Build LinkedIn jobs search URL
        search_url = (
            f"{LINKEDIN_URL}/jobs/search/?"
            f"keywords={job_title.replace(' ', '%20')}"
            f"&location={location.replace(' ', '%20')}"
            f"&f_TPR=r86400"   # Posted in last 24 hours
            f"&f_LF=f_AL"      # Easy Apply filter
        )

        await page.goto(search_url, wait_until="domcontentloaded")
        await human_delay(2000, 3500)

        # Collect job cards
        job_cards = await page.query_selector_all(".job-card-container")
        print(f"  Found {len(job_cards)} job cards.")

        for card in job_cards[:max_jobs]:
            try:
                title_el   = await card.query_selector(".job-card-list__title")
                company_el = await card.query_selector(".job-card-container__primary-description")
                link_el    = await card.query_selector("a.job-card-list__title")

                title   = await title_el.inner_text()   if title_el   else "Unknown"
                company = await company_el.inner_text() if company_el else "Unknown"
                url     = await link_el.get_attribute("href") if link_el else ""

                if url and not url.startswith("http"):
                    url = LINKEDIN_URL + url

                results.append({
                    "title":   title.strip(),
                    "company": company.strip(),
                    "location": location,
                    "url":     url,
                    "jd_text": "",
                    "portal":  "linkedin",
                    "applied": False,
                })
                await human_delay(300, 600)
            except Exception as e:
                print(f"  Skipping card: {e}")
                continue

    print(f"\n  Total jobs collected: {len(results)}")
    return results[:max_jobs]


# ─── Step 3: Extract JD ───────────────────────────────────────────────────────
async def extract_jd_linkedin(page, job: dict) -> str:
    """Open each job listing and extract the full job description text."""
    if not job["url"]:
        return ""
    try:
        await page.goto(job["url"], wait_until="domcontentloaded")
        await human_delay(2000, 3000)

        # Expand "Show more" if present
        try:
            show_more = await page.query_selector(".jobs-description__footer-button")
            if show_more:
                await show_more.click()
                await human_delay(500, 900)
        except Exception:
            pass

        jd_el = await page.query_selector(".jobs-description__content")
        if jd_el:
            jd_text = await jd_el.inner_text()
            return jd_text.strip()
    except Exception as e:
        print(f"  JD extraction error for {job['title']}: {e}")
    return ""


# ─── Step 4 & 5: Score & Tailored Resume (via main job_assistant logic) ───────
def score_and_prepare(job: dict, resume_path: str, api_key: str, config: dict) -> dict:
    """
    Score the JD against the resume and generate tailored documents
    if the ATS score exceeds the threshold.
    """
    from scripts.job_assistant import (
        jd_analysis, update_resume_docx, generate_cover_letter,
        save_cover_letter_pdf, get_company_initials, read_file
    )

    resume_text = read_file(resume_path)
    initials = get_company_initials(job["company"])
    threshold = config["filters"].get("min_ats_score_to_apply", 6.5)

    print(f"  Analysing JD for {job['company']} ...")
    analysis = jd_analysis(resume_text, job["jd_text"], api_key)

    # Extract overall score from analysis text
    score_match = re.search(r"Overall Result.*?(\d+\.?\d*)\s*/\s*10", analysis, re.IGNORECASE)
    ats_score = float(score_match.group(1)) if score_match else 0.0
    job["ats_score"] = ats_score
    print(f"  ATS Score: {ats_score}/10  (threshold: {threshold})")

    if ats_score < threshold:
        print(f"  Score below threshold — skipping application.")
        job["skip_reason"] = f"ATS score {ats_score} < {threshold}"
        return job

    print(f"  Generating tailored resume (DOCX) ...")
    resume_out = update_resume_docx(resume_path, job["jd_text"], api_key, initials)
    job["resume_path"] = str(resume_out)

    print(f"  Generating cover letter ...")
    prefs = config.get("candidate", {})
    position = job["title"]
    cover_text  = generate_cover_letter(
        resume_text, job["jd_text"], job["company"], position, api_key
    )
    cover_path  = save_cover_letter_pdf(cover_text, initials)
    job["cover_path"] = str(cover_path)

    return job


# ─── Step 6: Easy Apply ───────────────────────────────────────────────────────
async def easy_apply_linkedin(page, job: dict, config: dict) -> bool:
    """
    Attempt LinkedIn Easy Apply on the job listing.
    Fills standard fields and attaches the tailored resume PDF.
    Returns True if application submitted successfully.

    NOTE: require_confirmation_before_apply in config will pause
    and ask you to confirm before final submission.
    """
    require_confirm = config["auto_apply"].get("require_confirmation_before_apply", True)

    try:
        await page.goto(job["url"], wait_until="domcontentloaded")
        await human_delay(2000, 3000)

        # Click Easy Apply button
        easy_apply_btn = await page.query_selector(".jobs-apply-button--top-card")
        if not easy_apply_btn:
            print(f"  No Easy Apply button found for {job['title']}.")
            return False

        await easy_apply_btn.click()
        await human_delay(1500, 2500)

        # ── Page 1: Contact info (usually pre-filled from profile) ──────────
        await _fill_easy_apply_form(page, job, config)

        # ── Ask for confirmation before final submit ─────────────────────────
        if require_confirm:
            print(f"\n  ⚠️  Ready to submit for: {job['title']} at {job['company']}")
            print(f"      Resume: {job.get('resume_path', 'N/A')}")
            confirm = input("  Submit this application? [y/N]: ").strip().lower()
            if confirm != "y":
                print("  Skipped by user.")
                await page.keyboard.press("Escape")
                return False

        # Click Submit / Review button
        submit_btn = await page.query_selector('button[aria-label="Submit application"]')
        if submit_btn:
            await submit_btn.click()
            await human_delay(2000, 3000)
            print(f"  Application submitted: {job['title']} at {job['company']}")
            return True
        else:
            print("  Submit button not found — manual review needed.")
            return False

    except Exception as e:
        print(f"  Easy Apply error: {e}")
        return False


async def _fill_easy_apply_form(page, job: dict, config: dict):
    """Fill common Easy Apply form fields."""
    cand = {
        "phone":   os.getenv("CANDIDATE_PHONE", ""),
        "notice":  os.getenv("CANDIDATE_NOTICE_PERIOD", "30"),
        "current_ctc": os.getenv("CANDIDATE_CURRENT_CTC", ""),
        "expected_ctc": os.getenv("CANDIDATE_EXPECTED_CTC", ""),
        "exp":     os.getenv("CANDIDATE_TOTAL_EXPERIENCE", "7"),
    }

    # Phone field
    phone_field = await page.query_selector('input[name*="phone"], input[id*="phone"]')
    if phone_field:
        val = await phone_field.input_value()
        if not val:
            await human_type(page, 'input[name*="phone"]', cand["phone"])

    # Upload tailored resume if a file upload input exists
    resume_path = job.get("resume_path")
    if resume_path and Path(resume_path).exists():
        try:
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(resume_path)
                await human_delay(1000, 1500)
                print(f"  Attached resume: {Path(resume_path).name}")
        except Exception as e:
            print(f"  Resume upload error: {e}")

    await human_delay(800, 1400)

    # Click "Next" through multi-step form until Submit appears
    for _ in range(5):
        next_btn = await page.query_selector(
            'button[aria-label="Continue to next step"], '
            'button[aria-label="Review your application"]'
        )
        if next_btn:
            await next_btn.click()
            await human_delay(1200, 2000)
        else:
            break


# ─── Step 7: Log Results ──────────────────────────────────────────────────────
def log_application(job: dict):
    """Append job application result to the daily log."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"applied_{date_str}.json"

    log = []
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))

    log.append({
        "timestamp": datetime.now().isoformat(),
        "title":     job.get("title"),
        "company":   job.get("company"),
        "portal":    job.get("portal"),
        "url":       job.get("url"),
        "ats_score": job.get("ats_score"),
        "applied":   job.get("applied", False),
        "skip_reason": job.get("skip_reason", ""),
        "resume_path": job.get("resume_path", ""),
    })

    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"  Logged to: {log_path.name}")


# ─── Main LinkedIn Runner ─────────────────────────────────────────────────────
async def run_linkedin_agent(resume_path: str, api_key: str):
    """
    Execute the full LinkedIn application pipeline.
    """
    config = load_config()

    print("\n  Starting LinkedIn Agent ...")
    playwright, context, page = await launch_browser("linkedin", headless=False)

    try:
        # 1. Login
        logged_in = await linkedin_login(page)
        if not logged_in:
            print("  Login failed. Exiting.")
            return

        # 2. Search
        jobs = await search_linkedin_jobs(page, config)
        if not jobs:
            print("  No jobs found.")
            return

        # 3. Extract JDs + 4. Score + 5. Prepare Resume + 6. Apply
        for i, job in enumerate(jobs, 1):
            print(f"\n  [{i}/{len(jobs)}] {job['title']} @ {job['company']}")

            # Extract JD
            jd_text = await extract_jd_linkedin(page, job)
            job["jd_text"] = jd_text

            # Skip if JD too short
            if len(jd_text) < config["filters"].get("skip_if_jd_too_short_chars", 200):
                print("  JD too short — skipping.")
                job["skip_reason"] = "JD too short"
                log_application(job)
                continue

            # Save raw JD
            company_letters = re.sub(r"[^A-Z]", "", job["company"].upper())
            initials = company_letters[:4]
            jd_save_path = JD_DIR / f"jd_{initials}_{datetime.now().strftime('%H%M%S')}.txt"
            jd_save_path.write_text(jd_text, encoding="utf-8")

            # Score & prepare
            job = score_and_prepare(job, resume_path, api_key, config)

            if job.get("skip_reason"):
                log_application(job)
                continue

            # Apply
            if config["auto_apply"]["enabled"]:
                applied = await easy_apply_linkedin(page, job, config)
                job["applied"] = applied

            log_application(job)
            await human_delay(3000, 6000)  # Pause between applications

        print("\n  LinkedIn Agent complete.")

    finally:
        await close_browser(playwright, context)
