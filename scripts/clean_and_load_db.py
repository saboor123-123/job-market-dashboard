"""
Data Cleaning & SQLite Loader
Cleans the raw job listings CSV and loads it into a SQLite database
with normalized tables for efficient querying.

Author: Muhammad Saboor
Project: Job Market Insights Dashboard
"""

import pandas as pd
import sqlite3
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
RAW_DATA = "C:/Users/ashai/job-market-dashboard/data/job_listings_raw.csv"
CLEAN_DATA = "C:/Users/ashai/job-market-dashboard/data/job_listings_clean.csv"
DB_PATH = "C:/Users/ashai/job-market-dashboard/database/job_market.db"


def clean_data(df):
    """Clean and validate the raw dataset."""
    print(f"Raw records: {len(df)}")

    # 1. Remove duplicates
    df = df.drop_duplicates(subset=["title", "company", "location", "date_posted"])
    print(f"After dedup: {len(df)}")

    # 2. Handle missing values
    df["salary_avg"] = df["salary_avg"].fillna(df["salary_avg"].median())
    df["experience_level"] = df["experience_level"].fillna("Not Specified")
    df["employment_type"] = df["employment_type"].fillna("Full-time")

    # 3. Standardize text
    df["title"] = df["title"].str.strip().str.title()
    df["company"] = df["company"].str.strip()
    df["location"] = df["location"].str.strip()

    # 4. Remove outlier salaries (below 15k or above 250k)
    df = df[(df["salary_avg"] >= 15000) & (df["salary_avg"] <= 250000)]
    print(f"After salary filter: {len(df)}")

    # 5. Parse dates
    df["date_posted"] = pd.to_datetime(df["date_posted"])

    # 6. Add derived columns
    df["month_posted"] = df["date_posted"].dt.strftime("%Y-%m")
    df["country"] = df["location"].apply(extract_country)
    df["num_skills"] = df["skills_required"].apply(lambda x: len(x.split("|")) if pd.notna(x) else 0)

    print(f"Clean records: {len(df)}")
    return df


def extract_country(location):
    """Extract country from location string."""
    if "Remote" in str(location):
        return "Remote"
    parts = str(location).split(",")
    return parts[-1].strip() if len(parts) > 1 else location


def create_database(df):
    """Create SQLite database with normalized tables."""
    # Remove existing DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ── Main jobs table ───────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE jobs (
            job_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            country TEXT,
            category TEXT,
            salary_avg INTEGER,
            salary_min INTEGER,
            salary_max INTEGER,
            experience_level TEXT,
            employment_type TEXT,
            date_posted TEXT,
            month_posted TEXT,
            is_remote BOOLEAN,
            num_skills INTEGER
        )
    """)

    # ── Skills table (normalized) ─────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE job_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            skill TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        )
    """)

    # ── Insert jobs ───────────────────────────────────────────────────────────
    jobs_df = df.drop(columns=["skills_required"])
    jobs_df["date_posted"] = jobs_df["date_posted"].dt.strftime("%Y-%m-%d")
    jobs_df.to_sql("jobs", conn, if_exists="append", index=False)

    # ── Insert skills (one row per job-skill pair) ────────────────────────────
    skills_rows = []
    for _, row in df.iterrows():
        if pd.notna(row["skills_required"]):
            for skill in row["skills_required"].split("|"):
                skills_rows.append({"job_id": row["job_id"], "skill": skill.strip()})

    skills_df = pd.DataFrame(skills_rows)
    skills_df.to_sql("job_skills", conn, if_exists="append", index=False)

    # ── Create indexes for fast queries ───────────────────────────────────────
    cursor.execute("CREATE INDEX idx_jobs_category ON jobs(category)")
    cursor.execute("CREATE INDEX idx_jobs_location ON jobs(location)")
    cursor.execute("CREATE INDEX idx_jobs_experience ON jobs(experience_level)")
    cursor.execute("CREATE INDEX idx_skills_skill ON job_skills(skill)")
    cursor.execute("CREATE INDEX idx_skills_job_id ON job_skills(job_id)")

    conn.commit()

    # ── Verify ────────────────────────────────────────────────────────────────
    print("\n--- Database Summary ---")
    for table in ["jobs", "job_skills"]:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count:,} rows")

    # Sample queries to verify
    print("\n--- Top 10 Skills by Demand ---")
    results = cursor.execute("""
        SELECT skill, COUNT(*) as demand
        FROM job_skills
        GROUP BY skill
        ORDER BY demand DESC
        LIMIT 10
    """).fetchall()
    for skill, count in results:
        print(f"  {skill}: {count}")

    print("\n--- Average Salary by Category ---")
    results = cursor.execute("""
        SELECT category, ROUND(AVG(salary_avg)) as avg_salary, COUNT(*) as jobs
        FROM jobs
        GROUP BY category
        ORDER BY avg_salary DESC
    """).fetchall()
    for cat, salary, jobs in results:
        print(f"  {cat}: ${salary:,.0f} ({jobs} jobs)")

    conn.close()
    print(f"\nDatabase saved to {DB_PATH}")


def main():
    # Load raw data
    df = pd.read_csv(RAW_DATA)

    # Clean
    df_clean = clean_data(df)

    # Save clean CSV
    df_clean.to_csv(CLEAN_DATA, index=False)
    print(f"Clean CSV saved to {CLEAN_DATA}")

    # Load into SQLite
    create_database(df_clean)


if __name__ == "__main__":
    main()
