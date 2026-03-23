"""
auto_apply.py
==============
Master orchestrator for the AI Job Assistant auto-apply pipeline.

Run this script to:
  - Load your master resume
  - Launch LinkedIn and/or Naukri agents
  - Search, score, tailor, and apply — all in one run

Usage:
    python auto_apply.py
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / "credentials" / ".env")

from scripts.job_assistant import read_file
from agents.linkedin_agent import run_linkedin_agent
from agents.naukri_agent   import run_naukri_agent

RESUMES_DIR = BASE_DIR / "resumes"


# ─── Menu ─────────────────────────────────────────────────────────────────────
def print_menu():
    print("\n" + "=" * 60)
    print("     AI JOB ASSISTANT — Auto Apply Agent")
    print("=" * 60)
    print("  1.  Run LinkedIn Agent Only")
    print("  2.  Run Naukri Agent Only")
    print("  3.  Run Both Agents (LinkedIn + Naukri)")
    print("  0.  Exit")
    print("=" * 60)


def pick_resume() -> str:
    files = sorted(RESUMES_DIR.glob("*.*"))
    if not files:
        print("  No resume found in /resumes/ — please add your master resume.")
        sys.exit(1)
    print("\n  Available resumes:")
    for i, f in enumerate(files, 1):
        print(f"    [{i}] {f.name}")
    choice = input("  Select resume number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        return str(files[int(choice) - 1])
    return str(files[0])


# ─── Main ─────────────────────────────────────────────────────────────────────
async def main():
    print("\n  AI Job Assistant — Auto Apply")
    print("  Candidate: Harshad Shinde")
    print("─" * 60)

    api_key = os.getenv("ANTHROPIC_API_KEY") or input(
        "  Enter Anthropic API key: "
    ).strip()

    resume_path = pick_resume()
    resume_text = read_file(resume_path)
    print(f"  Master resume loaded: {Path(resume_path).name} ({len(resume_text):,} chars)")

    while True:
        print_menu()
        choice = input("  Select option: ").strip()

        if choice == "0":
            print("\n  Goodbye, Harshad! Good luck!\n")
            break
        elif choice == "1":
            await run_linkedin_agent(resume_path, api_key)
        elif choice == "2":
            await run_naukri_agent(resume_path, api_key)
        elif choice == "3":
            print("\n  Running LinkedIn agent first ...")
            await run_linkedin_agent(resume_path, api_key)
            print("\n  Running Naukri agent ...")
            await run_naukri_agent(resume_path, api_key)
            print("\n  Both agents complete.")
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    asyncio.run(main())
