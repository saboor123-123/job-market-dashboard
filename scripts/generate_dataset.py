"""
Job Market Dataset Generator
Generates a realistic dataset of 5,000+ tech job listings
for analysis and visualization.

Author: Muhammad Saboor
Project: Job Market Insights Dashboard
"""

import pandas as pd
import random
import csv
from datetime import datetime, timedelta

random.seed(42)

# ── Realistic job data pools ─────────────────────────────────────────────────

JOB_TITLES = {
    "Data Analyst": {"min_salary": 55000, "max_salary": 95000, "category": "Data"},
    "Junior Data Analyst": {"min_salary": 45000, "max_salary": 70000, "category": "Data"},
    "Senior Data Analyst": {"min_salary": 85000, "max_salary": 130000, "category": "Data"},
    "Data Scientist": {"min_salary": 80000, "max_salary": 150000, "category": "Data"},
    "Junior Data Scientist": {"min_salary": 65000, "max_salary": 95000, "category": "Data"},
    "Senior Data Scientist": {"min_salary": 120000, "max_salary": 180000, "category": "Data"},
    "Machine Learning Engineer": {"min_salary": 100000, "max_salary": 180000, "category": "Data"},
    "Data Engineer": {"min_salary": 90000, "max_salary": 160000, "category": "Data"},
    "Business Intelligence Analyst": {"min_salary": 60000, "max_salary": 110000, "category": "Data"},
    "Software Developer": {"min_salary": 70000, "max_salary": 140000, "category": "Software"},
    "Junior Software Developer": {"min_salary": 50000, "max_salary": 80000, "category": "Software"},
    "Senior Software Developer": {"min_salary": 110000, "max_salary": 170000, "category": "Software"},
    "Full Stack Developer": {"min_salary": 75000, "max_salary": 145000, "category": "Software"},
    "Frontend Developer": {"min_salary": 65000, "max_salary": 130000, "category": "Software"},
    "Backend Developer": {"min_salary": 75000, "max_salary": 145000, "category": "Software"},
    "DevOps Engineer": {"min_salary": 90000, "max_salary": 160000, "category": "Software"},
    "IT Support Specialist": {"min_salary": 40000, "max_salary": 65000, "category": "IT Support"},
    "Help Desk Technician": {"min_salary": 35000, "max_salary": 55000, "category": "IT Support"},
    "System Administrator": {"min_salary": 60000, "max_salary": 100000, "category": "IT Support"},
    "Network Administrator": {"min_salary": 55000, "max_salary": 95000, "category": "IT Support"},
    "Cybersecurity Analyst": {"min_salary": 75000, "max_salary": 130000, "category": "Cybersecurity"},
    "Cloud Engineer": {"min_salary": 95000, "max_salary": 165000, "category": "Cloud"},
    "QA Engineer": {"min_salary": 55000, "max_salary": 100000, "category": "Software"},
    "Database Administrator": {"min_salary": 65000, "max_salary": 115000, "category": "Data"},
    "Web Developer": {"min_salary": 50000, "max_salary": 100000, "category": "Software"},
    "AI Engineer": {"min_salary": 110000, "max_salary": 200000, "category": "Data"},
    "Product Analyst": {"min_salary": 70000, "max_salary": 120000, "category": "Data"},
    "UX Designer": {"min_salary": 60000, "max_salary": 120000, "category": "Design"},
}

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Spotify",
    "Salesforce", "Adobe", "IBM", "Oracle", "SAP", "Atlassian", "Canva",
    "Shopify", "Stripe", "Datadog", "Snowflake", "Databricks", "Palantir",
    "Accenture", "Deloitte", "PwC", "KPMG", "EY", "McKinsey",
    "JPMorgan Chase", "Goldman Sachs", "Commonwealth Bank", "ANZ",
    "NAB", "Westpac", "Telstra", "Optus", "Woolworths Group",
    "TechCorp Solutions", "DataVibe Analytics", "CloudFirst Inc",
    "NexGen Systems", "ByteShift Labs", "Quantum Leap Tech",
    "PivotPoint Data", "Horizon Digital", "BlueWave Software",
    "GreenField Analytics", "Summit AI", "ClearPath Technologies",
    "StartupXYZ", "InnoTech", "FutureMind", "CodeCraft Studios",
]

LOCATIONS = {
    "Sydney, Australia": 0.18,
    "Melbourne, Australia": 0.16,
    "Brisbane, Australia": 0.08,
    "Perth, Australia": 0.05,
    "Adelaide, Australia": 0.04,
    "Canberra, Australia": 0.03,
    "Remote": 0.15,
    "New York, USA": 0.06,
    "San Francisco, USA": 0.05,
    "London, UK": 0.05,
    "Toronto, Canada": 0.04,
    "Singapore": 0.04,
    "Berlin, Germany": 0.03,
    "Bangalore, India": 0.04,
}

SKILLS_BY_CATEGORY = {
    "Data": ["Python", "SQL", "Excel", "Tableau", "Power BI", "R", "Pandas",
             "NumPy", "Scikit-learn", "TensorFlow", "Spark", "Hadoop",
             "Statistics", "Machine Learning", "Data Visualization",
             "Jupyter", "Git", "AWS", "Azure", "Google Cloud"],
    "Software": ["Python", "JavaScript", "TypeScript", "React", "Node.js",
                 "Java", "C#", ".NET", "SQL", "Git", "Docker", "Kubernetes",
                 "AWS", "Azure", "REST APIs", "GraphQL", "Agile", "CI/CD",
                 "HTML/CSS", "MongoDB"],
    "IT Support": ["Windows Server", "Linux", "Active Directory", "Networking",
                   "TCP/IP", "DNS", "DHCP", "Troubleshooting", "Help Desk",
                   "ITIL", "Office 365", "Azure AD", "PowerShell", "Backup"],
    "Cybersecurity": ["Network Security", "Firewalls", "SIEM", "Penetration Testing",
                      "Python", "Linux", "Incident Response", "Compliance",
                      "Risk Assessment", "Encryption", "AWS Security"],
    "Cloud": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes",
              "Terraform", "CI/CD", "Linux", "Python", "Networking",
              "Serverless", "CloudFormation"],
    "Design": ["Figma", "Sketch", "Adobe XD", "HTML/CSS", "JavaScript",
               "User Research", "Wireframing", "Prototyping", "Accessibility"],
}

EXPERIENCE_LEVELS = {
    "Entry Level": 0.25,
    "Mid Level": 0.40,
    "Senior Level": 0.25,
    "Lead/Manager": 0.10,
}

EMPLOYMENT_TYPES = {
    "Full-time": 0.60,
    "Part-time": 0.15,
    "Contract": 0.15,
    "Internship": 0.10,
}


def weighted_choice(choices_dict):
    """Pick a random item based on weights."""
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return random.choices(items, weights=weights, k=1)[0]


def generate_job_listing(job_id):
    """Generate a single realistic job listing."""
    title = random.choice(list(JOB_TITLES.keys()))
    info = JOB_TITLES[title]
    category = info["category"]

    # Salary with some randomness
    salary_min = info["min_salary"] + random.randint(-5000, 5000)
    salary_max = info["max_salary"] + random.randint(-5000, 10000)
    salary_avg = (salary_min + salary_max) // 2

    # Adjust salary for location
    location = weighted_choice(LOCATIONS)
    if "San Francisco" in location or "New York" in location:
        salary_avg = int(salary_avg * 1.2)
    elif "Sydney" in location or "Melbourne" in location:
        salary_avg = int(salary_avg * 1.05)
    elif "Bangalore" in location:
        salary_avg = int(salary_avg * 0.5)
    elif "Remote" in location:
        salary_avg = int(salary_avg * 0.95)

    # Pick 3-6 required skills
    skill_pool = SKILLS_BY_CATEGORY.get(category, SKILLS_BY_CATEGORY["Software"])
    num_skills = random.randint(3, min(6, len(skill_pool)))
    skills = random.sample(skill_pool, num_skills)

    # Random date in the last 6 months
    days_ago = random.randint(0, 180)
    posted_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    # Experience level
    experience = weighted_choice(EXPERIENCE_LEVELS)
    if "Junior" in title or "Intern" in title:
        experience = "Entry Level"
    elif "Senior" in title or "Lead" in title:
        experience = random.choice(["Senior Level", "Lead/Manager"])

    # Employment type
    emp_type = weighted_choice(EMPLOYMENT_TYPES)

    # Company
    company = random.choice(COMPANIES)

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "category": category,
        "salary_avg": salary_avg,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "experience_level": experience,
        "employment_type": emp_type,
        "skills_required": "|".join(skills),
        "date_posted": posted_date,
        "is_remote": location == "Remote",
    }


def main():
    """Generate the full dataset."""
    print("Generating 5,000 job listings...")

    jobs = []
    for i in range(1, 5001):
        jobs.append(generate_job_listing(i))

    df = pd.DataFrame(jobs)

    # Save as CSV
    output_path = "C:/Users/ashai/job-market-dashboard/data/job_listings_raw.csv"
    df.to_csv(output_path, index=False)

    print(f"Dataset saved to {output_path}")
    print(f"Total records: {len(df)}")
    print(f"\nSample data:")
    print(df.head(10).to_string())
    print(f"\nCategories: {df['category'].value_counts().to_dict()}")
    print(f"Locations: {df['location'].nunique()} unique locations")
    print(f"Salary range: ${df['salary_avg'].min():,} - ${df['salary_avg'].max():,}")


if __name__ == "__main__":
    main()
