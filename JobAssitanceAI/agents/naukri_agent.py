"""
naukri_agent.py
================
Automates Naukri job search and application.

Flow:
  1. Login to naukri.com (session cached after first run)
  2. Search jobs using job_preferences.json
  3. Extract full JD from each listing
  4. Score + generate tailored resume + cover letter via Claude
  5. Apply to job (attaches resume, fills form)
  6. Log all activity
"""

import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from agents.browser_base import launch_browser, close_browser, human_delay, human_type

load_dotenv(Path(__file__).parent.parent / "credentials" / ".env")

BASE_DIR    = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "job_preferences.json"
LOG_DIR     = BASE_DIR / "results" / "applied_jobs"
JD_DIR      = BASE_DIR / "results" / "jd_extracted"
LOG_DIR.mkdir(parents=True, exist_ok=True)
JD_DIR.mkdir(parents=True, exist_ok=True)

NAUKRI_URL = "https://www.naukri.com"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


# ─── Step 1: Login ────────────────────────────────────────────────────────────
async def naukri_login(page) -> bool:
    """Login to Naukri. Session is saved so login is needed only once."""
    await page.goto(NAUKRI_URL, wait_until="domcontentloaded")
    await human_delay(2000, 3000)

    # Check if already logged in (profile icon visible)
    try:
        profile = await page.query_selector(".nI-gNb-drawer__bars")
        if profile:
            print("  Already logged in to Naukri (session active).")
            return True
    except Exception:
        pass

    print("  Logging in to Naukri ...")

    # Click Login
    try:
        login_btn = await page.query_selector('a[href*="login"]')
        if login_btn:
            await login_btn.click()
            await human_delay(1500, 2500)
    except Exception:
        await page.goto(f"{NAUKRI_URL}/nlogin/login", wait_until="domcontentloaded")
        await human_delay(1500, 2000)

    email    = os.getenv("NAUKRI_EMAIL")
    password = os.getenv("NAUKRI_PASSWORD")

    try:
        await human_type(page, 'input[placeholder*="Enter your active Email ID"]', email)
        await human_delay(500, 900)
        await human_type(page, 'input[placeholder*="Enter your password"]', password)
        await human_delay(600, 1000)
        await page.keyboard.press("Enter")
        await human_delay(3000, 5000)
        print("  Naukri login successful.")
        return True
    except Exception as e:
        print(f"  Login form interaction failed: {e}")
        print("  Please log in manually in the browser window, then press Enter.")
        input("  [Press Enter after manual login] > ")
        return True


# ─── Step 2: Search Jobs ──────────────────────────────────────────────────────
async def search_naukri_jobs(page, config: dict) -> list:
    """
    Search jobs on Naukri using configured job titles and location.
    Returns list of job dicts.
    """
    prefs    = config["search"]
    results  = []
    max_jobs = prefs.get("max_jobs_per_run", 10)

    for job_title in prefs["job_titles"]:
        if len(results) >= max_jobs:
            break

        location = prefs["locations"][0]
        exp_min  = prefs["experience_years"]["min"]
        exp_max  = prefs["experience_years"]["max"]

        print(f"\n  Searching Naukri: '{job_title}' in '{location}' ...")

        # Naukri search URL
        search_url = (
            f"{NAUKRI_URL}/{job_title.lower().replace(' ', '-')}-jobs"
            f"?k={job_title.replace(' ', '%20')}"
            f"&l={location.replace(' ', '%20')}"
            f"&experience={exp_min}"
        )

        await page.goto(search_url, wait_until="domcontentloaded")
        await human_delay(2500, 4000)

        # Job cards
        job_cards = await page.query_selector_all("article.jobTuple")
        print(f"  Found {len(job_cards)} listings.")

        for card in job_cards:
            try:
                title_el   = await card.query_selector("a.title")
                company_el = await card.query_selector("a.subTitle")
                loc_el     = await card.query_selector("li.location")

                title    = await title_el.inner_text()   if title_el   else "Unknown"
                company  = await company_el.inner_text() if company_el else "Unknown"
                location_text = await loc_el.inner_text() if loc_el else location
                url      = await title_el.get_attribute("href") if title_el else ""

                results.append({
                    "title":    title.strip(),
                    "company":  company.strip(),
                    "location": location_text.strip(),
                    "url":      url,
                    "jd_text":  "",
                    "portal":   "naukri",
                    "applied":  False,
                })
                await human_delay(200, 500)
            except Exception as e:
                print(f"  Card error: {e}")
                continue

    print(f"\n  Total Naukri jobs collected: {len(results)}")
    return results[:max_jobs]


# ─── Step 3: Extract JD ───────────────────────────────────────────────────────
async def extract_jd_naukri(page, job: dict) -> str:
    """Navigate to job page and extract the full job description."""
    if not job["url"]:
        return ""
    try:
        await page.goto(job["url"], wait_until="domcontentloaded")
        await human_delay(2000, 3500)

        # Try multiple possible JD selectors (Naukri updates layout often)
        selectors = [
            ".job-desc",
            ".JDC_desc",
            "section.styles_job-desc-container__txpYf",
            ".dang-inner-html",
        ]
        for sel in selectors:
            el = await page.query_selector(sel)
            if el:
                text = await el.inner_text()
                if text and len(text) > 100:
                    return text.strip()

    except Exception as e:
        print(f"  Naukri JD extraction error: {e}")
    return ""


# ─── Step 4 & 5: Score & Prepare (reuses job_assistant.py functions) ──────────
def score_and_prepare_naukri(job: dict, resume_path: str, api_key: str, config: dict) -> dict:
    """Score and generate tailored documents — same logic as LinkedIn agent."""
    import sys
    sys.path.insert(0, str(BASE_DIR / "Scripts"))
    from job_assistant import (
        jd_analysis, update_resume_docx, generate_cover_letter,
        save_cover_letter_pdf, get_company_initials, read_file
    )

    resume_text = read_file(resume_path)
    initials  = get_company_initials(job["company"])
    threshold = config["filters"].get("min_ats_score_to_apply", 6.5)

    print(f"  Analysing JD: {job['company']} ...")
    analysis = jd_analysis(resume_text, job["jd_text"], api_key)

    score_match = re.search(r"Overall Result.*?(\d+\.?\d*)\s*/\s*10", analysis, re.IGNORECASE)
    ats_score   = float(score_match.group(1)) if score_match else 0.0
    job["ats_score"] = ats_score
    print(f"  ATS Score: {ats_score}/10")

    if ats_score < threshold:
        job["skip_reason"] = f"ATS score {ats_score} < {threshold}"
        print(f"  Below threshold — skipping.")
        return job

    resume_out = update_resume_docx(resume_path, job["jd_text"], api_key, initials)
    job["resume_path"] = str(resume_out)

    cover_text = generate_cover_letter(
        resume_text, job["jd_text"], job["company"], job["title"], api_key
    )
    job["cover_path"] = str(save_cover_letter_pdf(cover_text, initials))
    return job


# ─── Step 6: Apply on Naukri ──────────────────────────────────────────────────
async def apply_naukri(page, job: dict, config: dict) -> bool:
    """
    Apply to a Naukri job listing.
    Uploads tailored resume and fills required fields.
    """
    require_confirm = config["auto_apply"].get("require_confirmation_before_apply", True)

    try:
        await page.goto(job["url"], wait_until="domcontentloaded")
        await human_delay(2000, 3000)

        # Click Apply button
        apply_btn = await page.query_selector('button#apply-button, a#apply-button, .apply-button')
        if not apply_btn:
            print(f"  No Apply button found for {job['title']}.")
            return False

        await apply_btn.click()
        await human_delay(2000, 3500)

        # Upload resume if file input appears
        resume_path = job.get("resume_path")
        if resume_path and Path(resume_path).exists():
            try:
                file_input = await page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(resume_path)
                    await human_delay(1500, 2500)
                    print(f"  Resume attached: {Path(resume_path).name}")
            except Exception as e:
                print(f"  Resume upload error: {e}")

        # Fill notice period if field present
        notice = os.getenv("CANDIDATE_NOTICE_PERIOD", "30")
        try:
            notice_field = await page.query_selector(
                'input[placeholder*="notice"], input[name*="notice"]'
            )
            if notice_field:
                await notice_field.fill(notice)
        except Exception:
            pass

        # Confirm before submitting
        if require_confirm:
            print(f"\n  Ready to submit: {job['title']} @ {job['company']}")
            confirm = input("  Submit? [y/N]: ").strip().lower()
            if confirm != "y":
                print("  Skipped.")
                return False

        # Click final submit
        submit = await page.query_selector(
            'button[type="submit"], button.apply-btn, button.submit-btn'
        )
        if submit:
            await submit.click()
            await human_delay(2000, 3000)
            print(f"  Applied: {job['title']} @ {job['company']}")
            return True

    except Exception as e:
        print(f"  Naukri apply error: {e}")
    return False


# ─── Logging ──────────────────────────────────────────────────────────────────
def log_application(job: dict):
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"applied_{date_str}.json"
    log = []
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
    log.append({
        "timestamp":   datetime.now().isoformat(),
        "title":       job.get("title"),
        "company":     job.get("company"),
        "portal":      job.get("portal"),
        "url":         job.get("url"),
        "ats_score":   job.get("ats_score"),
        "applied":     job.get("applied", False),
        "skip_reason": job.get("skip_reason", ""),
        "resume_path": job.get("resume_path", ""),
    })
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"  Logged.")


# ─── Main Naukri Runner ───────────────────────────────────────────────────────
async def run_naukri_agent(resume_path: str, api_key: str):
    """Full Naukri automation pipeline."""
    config = load_config()

    print("\n  Starting Naukri Agent ...")
    playwright, context, page = await launch_browser("naukri", headless=False)

    try:
        if not await naukri_login(page):
            print("  Login failed.")
            return

        jobs = await search_naukri_jobs(page, config)
        if not jobs:
            print("  No jobs found.")
            return

        for i, job in enumerate(jobs, 1):
            print(f"\n  [{i}/{len(jobs)}] {job['title']} @ {job['company']}")

            jd_text = await extract_jd_naukri(page, job)
            job["jd_text"] = jd_text

            if len(jd_text) < config["filters"].get("skip_if_jd_too_short_chars", 200):
                job["skip_reason"] = "JD too short"
                log_application(job)
                continue

            job = score_and_prepare_naukri(job, resume_path, api_key, config)

            if job.get("skip_reason"):
                log_application(job)
                continue

            if config["auto_apply"]["enabled"]:
                applied = await apply_naukri(page, job, config)
                job["applied"] = applied

            log_application(job)
            await human_delay(4000, 7000)

        print("\n  Naukri Agent complete.")

    finally:
        await close_browser(playwright, context)
