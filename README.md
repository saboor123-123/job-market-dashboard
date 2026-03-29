# Job Market Insights Dashboard

An end-to-end data analytics project that collects, cleans, analyzes, and visualizes **5,000+ tech job listings** across 14 global locations. Built to uncover hiring trends, salary insights, and in-demand skills in the tech industry.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?logo=sqlite)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)
![HTML/CSS](https://img.shields.io/badge/HTML%2FCSS-Dashboard-orange?logo=html5)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?logo=pandas)

---

## Live Dashboard Preview

The interactive dashboard visualizes key findings including:
- Top in-demand skills (Python, AWS, SQL lead the market)
- Salary distributions by role, experience level, and location
- Job category breakdowns with donut charts
- Monthly posting trends
- Entry-level opportunity analysis

---

## Project Architecture

```
job-market-dashboard/
|
|-- data/
|   |-- job_listings_raw.csv        # Raw generated dataset (5,000 records)
|   |-- job_listings_clean.csv      # Cleaned & validated dataset
|
|-- database/
|   |-- job_market.db               # SQLite database with normalized tables
|
|-- scripts/
|   |-- generate_dataset.py         # Dataset generation with realistic distributions
|   |-- clean_and_load_db.py        # Data cleaning pipeline + SQLite loader
|   |-- analyze_and_export.py       # Analysis queries + JSON/Excel export
|
|-- dashboard/
|   |-- index.html                  # Interactive web dashboard
|   |-- css/style.css               # Custom dark theme styling
|   |-- js/app.js                   # Dashboard rendering logic
|   |-- js/data.json                # Analysis results for frontend
|
|-- reports/
|   |-- job_market_report.xlsx      # Excel report with multiple analysis sheets
|
|-- resume/
|   |-- index.html                  # Professional resume (HTML/CSS)
|
|-- README.md
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Generation** | Python, Random | Create realistic job market dataset |
| **Data Cleaning** | Pandas | Deduplication, validation, type conversion |
| **Database** | SQLite | Normalized storage with indexed queries |
| **Analysis** | SQL, Pandas | Aggregations, salary analysis, trend detection |
| **Visualization** | HTML, CSS, JavaScript | Interactive dashboard with charts |
| **Reporting** | OpenPyXL | Multi-sheet Excel report export |

---

## Key Findings

| Insight | Details |
|---------|---------|
| **#1 In-Demand Skill** | Python (found in 976 job listings) |
| **Highest Paying Category** | Cloud Engineering ($133K avg) |
| **Remote Work** | 15.2% of all positions |
| **Best Entry-Level Role** | Junior Software Developer (208 openings) |
| **Top Salary Premium Skill** | CloudFormation ($133K avg salary) |

---

## How to Run

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/saboor123-123/job-market-dashboard.git
cd job-market-dashboard

# Install dependencies
pip install pandas openpyxl

# Step 1: Generate the dataset
python scripts/generate_dataset.py

# Step 2: Clean data and load into SQLite
python scripts/clean_and_load_db.py

# Step 3: Run analysis and export results
python scripts/analyze_and_export.py

# Step 4: Open the dashboard
# Open dashboard/index.html in your browser
# Or use a local server:
npx serve dashboard
```

---

## Data Pipeline

```
Raw Data Generation     Data Cleaning          SQLite Database
 (Python/Random)   -->  (Pandas)          -->  (Normalized Tables)
                                                      |
                                                      v
  Excel Report     <--  Analysis/Export   <--  SQL Queries
  (OpenPyXL)            (JSON for Web)         (Aggregations)
                              |
                              v
                     Interactive Dashboard
                     (HTML/CSS/JavaScript)
```

---

## Skills Demonstrated

- **Python**: Data generation, cleaning, analysis scripting
- **SQL**: Database design, complex queries, indexing, JOINs
- **Pandas**: DataFrame operations, data cleaning, type handling
- **JavaScript**: DOM manipulation, async data loading, dynamic rendering
- **HTML/CSS**: Responsive design, CSS Grid, animations, dark theme
- **Data Visualization**: Bar charts, donut charts, trend lines, data tables
- **Database Design**: Normalized schema, foreign keys, indexing strategy
- **Excel Reporting**: Multi-sheet workbooks with formatted data

---

## Author

**Muhammad Saboor**
- Currently studying Bachelor of Data Science at Victoria University
- Diploma of Information Technology
- Based in Melbourne, Australia
- Passionate about turning data into actionable insights
- GitHub: [saboor123-123](https://github.com/saboor123-123)
- Email: bmuhammadsaboor@gmail.com

---

## License

MIT License - feel free to use this as a template for your own portfolio projects.
