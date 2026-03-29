"""
Data Analysis & JSON Export
Queries SQLite database, performs analysis, and exports
results as JSON files for the web dashboard.

Author: Muhammad Saboor
Project: Job Market Insights Dashboard
"""

import sqlite3
import json
import pandas as pd
from collections import Counter

DB_PATH = "C:/Users/ashai/job-market-dashboard/database/job_market.db"
JSON_OUT = "C:/Users/ashai/job-market-dashboard/dashboard/js/data.json"
EXCEL_OUT = "C:/Users/ashai/job-market-dashboard/reports/job_market_report.xlsx"


def query_db(query, params=None):
    """Execute a query and return results as list of dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params or [])
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def analyze():
    """Run all analyses and return a dashboard data dict."""
    dashboard = {}

    # ── 1. Overview Stats ─────────────────────────────────────────────────────
    overview = query_db("""
        SELECT
            COUNT(*) as total_jobs,
            COUNT(DISTINCT company) as total_companies,
            COUNT(DISTINCT location) as total_locations,
            ROUND(AVG(salary_avg)) as avg_salary,
            ROUND(MIN(salary_avg)) as min_salary,
            ROUND(MAX(salary_avg)) as max_salary,
            SUM(CASE WHEN is_remote = 1 THEN 1 ELSE 0 END) as remote_jobs
        FROM jobs
    """)[0]
    dashboard["overview"] = overview

    # ── 2. Top 15 Skills by Demand ────────────────────────────────────────────
    dashboard["top_skills"] = query_db("""
        SELECT skill as name, COUNT(*) as count
        FROM job_skills
        GROUP BY skill
        ORDER BY count DESC
        LIMIT 15
    """)

    # ── 3. Jobs by Category ───────────────────────────────────────────────────
    dashboard["jobs_by_category"] = query_db("""
        SELECT category as name, COUNT(*) as count, ROUND(AVG(salary_avg)) as avg_salary
        FROM jobs
        GROUP BY category
        ORDER BY count DESC
    """)

    # ── 4. Average Salary by Job Title (Top 15) ──────────────────────────────
    dashboard["salary_by_title"] = query_db("""
        SELECT title as name, ROUND(AVG(salary_avg)) as avg_salary, COUNT(*) as count
        FROM jobs
        GROUP BY title
        ORDER BY avg_salary DESC
        LIMIT 15
    """)

    # ── 5. Jobs by Location ───────────────────────────────────────────────────
    dashboard["jobs_by_location"] = query_db("""
        SELECT location as name, COUNT(*) as count, ROUND(AVG(salary_avg)) as avg_salary
        FROM jobs
        GROUP BY location
        ORDER BY count DESC
    """)

    # ── 6. Salary Distribution by Experience Level ────────────────────────────
    dashboard["salary_by_experience"] = query_db("""
        SELECT
            experience_level as name,
            ROUND(AVG(salary_avg)) as avg_salary,
            ROUND(MIN(salary_avg)) as min_salary,
            ROUND(MAX(salary_avg)) as max_salary,
            COUNT(*) as count
        FROM jobs
        GROUP BY experience_level
        ORDER BY avg_salary DESC
    """)

    # ── 7. Employment Type Distribution ───────────────────────────────────────
    dashboard["employment_types"] = query_db("""
        SELECT employment_type as name, COUNT(*) as count
        FROM jobs
        GROUP BY employment_type
        ORDER BY count DESC
    """)

    # ── 8. Monthly Job Posting Trends ─────────────────────────────────────────
    dashboard["monthly_trends"] = query_db("""
        SELECT month_posted as month, COUNT(*) as count
        FROM jobs
        GROUP BY month_posted
        ORDER BY month_posted ASC
    """)

    # ── 9. Remote vs On-site ──────────────────────────────────────────────────
    dashboard["remote_stats"] = query_db("""
        SELECT
            CASE WHEN is_remote = 1 THEN 'Remote' ELSE 'On-site' END as name,
            COUNT(*) as count,
            ROUND(AVG(salary_avg)) as avg_salary
        FROM jobs
        GROUP BY is_remote
    """)

    # ── 10. Top Hiring Companies ──────────────────────────────────────────────
    dashboard["top_companies"] = query_db("""
        SELECT company as name, COUNT(*) as count, ROUND(AVG(salary_avg)) as avg_salary
        FROM jobs
        GROUP BY company
        ORDER BY count DESC
        LIMIT 15
    """)

    # ── 11. Skills Salary Premium (which skills pay more) ─────────────────────
    dashboard["skills_salary"] = query_db("""
        SELECT js.skill as name, ROUND(AVG(j.salary_avg)) as avg_salary, COUNT(*) as count
        FROM job_skills js
        JOIN jobs j ON js.job_id = j.job_id
        GROUP BY js.skill
        HAVING count >= 50
        ORDER BY avg_salary DESC
        LIMIT 15
    """)

    # ── 12. Entry Level Jobs (most relevant for the user) ─────────────────────
    dashboard["entry_level_jobs"] = query_db("""
        SELECT title as name, COUNT(*) as count, ROUND(AVG(salary_avg)) as avg_salary
        FROM jobs
        WHERE experience_level = 'Entry Level'
        GROUP BY title
        ORDER BY count DESC
        LIMIT 10
    """)

    # ── 13. Skills for Entry Level Data Roles ─────────────────────────────────
    dashboard["entry_level_data_skills"] = query_db("""
        SELECT js.skill as name, COUNT(*) as count
        FROM job_skills js
        JOIN jobs j ON js.job_id = j.job_id
        WHERE j.experience_level = 'Entry Level' AND j.category = 'Data'
        GROUP BY js.skill
        ORDER BY count DESC
        LIMIT 10
    """)

    return dashboard


def export_excel(dashboard):
    """Export analysis results to Excel with multiple sheets."""
    with pd.ExcelWriter(EXCEL_OUT, engine="openpyxl") as writer:
        # Overview
        pd.DataFrame([dashboard["overview"]]).to_excel(writer, sheet_name="Overview", index=False)

        # Top Skills
        pd.DataFrame(dashboard["top_skills"]).to_excel(writer, sheet_name="Top Skills", index=False)

        # Salary by Title
        pd.DataFrame(dashboard["salary_by_title"]).to_excel(writer, sheet_name="Salary by Title", index=False)

        # Jobs by Location
        pd.DataFrame(dashboard["jobs_by_location"]).to_excel(writer, sheet_name="Jobs by Location", index=False)

        # Jobs by Category
        pd.DataFrame(dashboard["jobs_by_category"]).to_excel(writer, sheet_name="Jobs by Category", index=False)

        # Top Companies
        pd.DataFrame(dashboard["top_companies"]).to_excel(writer, sheet_name="Top Companies", index=False)

        # Entry Level Opportunities
        pd.DataFrame(dashboard["entry_level_jobs"]).to_excel(writer, sheet_name="Entry Level Jobs", index=False)

        # Skills Salary Premium
        pd.DataFrame(dashboard["skills_salary"]).to_excel(writer, sheet_name="Skills Salary Premium", index=False)

    print(f"Excel report saved to {EXCEL_OUT}")


def main():
    print("Running analysis...")
    dashboard = analyze()

    # Save JSON for web dashboard
    with open(JSON_OUT, "w") as f:
        json.dump(dashboard, f, indent=2)
    print(f"Dashboard JSON saved to {JSON_OUT}")

    # Save Excel report
    export_excel(dashboard)

    # Print key insights
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)

    o = dashboard["overview"]
    print(f"\nTotal Jobs Analyzed: {o['total_jobs']:,}")
    print(f"Companies: {o['total_companies']}")
    print(f"Average Salary: ${o['avg_salary']:,.0f}")
    print(f"Remote Jobs: {o['remote_jobs']} ({o['remote_jobs']/o['total_jobs']*100:.1f}%)")

    print(f"\nTop 5 In-Demand Skills:")
    for s in dashboard["top_skills"][:5]:
        print(f"  {s['name']}: {s['count']} job listings")

    print(f"\nHighest Paying Skills:")
    for s in dashboard["skills_salary"][:5]:
        print(f"  {s['name']}: ${s['avg_salary']:,.0f} avg")

    print(f"\nBest Entry-Level Opportunities:")
    for j in dashboard["entry_level_jobs"][:5]:
        print(f"  {j['name']}: {j['count']} openings, ${j['avg_salary']:,.0f} avg salary")


if __name__ == "__main__":
    main()
