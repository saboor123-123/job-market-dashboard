/**
 * Job Market Insights Dashboard
 * Interactive visualization of 5,000+ tech job listings
 * Built with vanilla JavaScript - no frameworks required
 *
 * Author: Muhammad Saboor
 * Tech: HTML, CSS, JavaScript, Chart.js
 */

// ── Global State ─────────────────────────────────────────────────────────────

let dashboardData = null;
let activeCategory = "All";

// ── Color Palette ────────────────────────────────────────────────────────────

const COLORS = {
    blue: "#3b82f6",
    green: "#22c55e",
    orange: "#f59e0b",
    purple: "#a855f7",
    red: "#ef4444",
    cyan: "#06b6d4",
    pink: "#ec4899",
    indigo: "#6366f1",
    teal: "#14b8a6",
    amber: "#f59e0b",
    lime: "#84cc16",
    rose: "#f43f5e",
    sky: "#0ea5e9",
    violet: "#8b5cf6",
    emerald: "#10b981",
};

const COLOR_ARRAY = Object.values(COLORS);

// ── Initialize ───────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("js/data.json");
        dashboardData = await response.json();
        renderDashboard();
    } catch (error) {
        console.error("Failed to load data:", error);
        document.querySelector(".container").innerHTML =
            '<p style="color: #ef4444; text-align:center; padding:40px;">Error loading data. Make sure data.json exists.</p>';
    }
});

// ── Main Render ──────────────────────────────────────────────────────────────

function renderDashboard() {
    const d = dashboardData;
    renderOverviewStats(d.overview);
    renderFilterBar(d.jobs_by_category);
    renderTopSkillsChart(d.top_skills);
    renderSalaryByTitleChart(d.salary_by_title);
    renderCategoryDonut(d.jobs_by_category);
    renderEmploymentDonut(d.employment_types);
    renderLocationTable(d.jobs_by_location);
    renderExperienceChart(d.salary_by_experience);
    renderSkillsSalaryChart(d.skills_salary);
    renderMonthlyTrends(d.monthly_trends);
    renderInsights(d);
    renderEntryLevelTable(d.entry_level_jobs, d.entry_level_data_skills);
}

// ── Overview Stats ───────────────────────────────────────────────────────────

function renderOverviewStats(overview) {
    const container = document.getElementById("stats-grid");
    const stats = [
        { label: "Total Jobs", value: formatNumber(overview.total_jobs), sub: "Across all categories", color: "blue" },
        { label: "Avg Salary", value: "$" + formatNumber(overview.avg_salary), sub: `$${formatNumber(overview.min_salary)} - $${formatNumber(overview.max_salary)}`, color: "green" },
        { label: "Companies", value: overview.total_companies, sub: `${overview.total_locations} locations`, color: "orange" },
        { label: "Remote Jobs", value: formatNumber(overview.remote_jobs), sub: `${((overview.remote_jobs / overview.total_jobs) * 100).toFixed(1)}% of all jobs`, color: "purple" },
    ];

    container.innerHTML = stats
        .map(
            (s, i) => `
        <div class="stat-card animate">
            <div class="label">${s.label}</div>
            <div class="value">${s.value}</div>
            <div class="sub">${s.sub}</div>
        </div>
    `
        )
        .join("");
}

// ── Filter Bar ───────────────────────────────────────────────────────────────

function renderFilterBar(categories) {
    const container = document.getElementById("filter-bar");
    const cats = ["All", ...categories.map((c) => c.name)];

    container.innerHTML = cats
        .map(
            (c) => `
        <button class="filter-btn ${c === activeCategory ? "active" : ""}"
                onclick="filterByCategory('${c}')">${c}</button>
    `
        )
        .join("");
}

function filterByCategory(category) {
    activeCategory = category;
    renderDashboard();
}

// ── Top Skills Bar Chart ─────────────────────────────────────────────────────

function renderTopSkillsChart(skills) {
    const container = document.getElementById("top-skills-chart");
    const maxVal = Math.max(...skills.map((s) => s.count));

    container.innerHTML = skills
        .slice(0, 12)
        .map(
            (s, i) => `
        <div class="bar-row animate" style="animation-delay: ${i * 0.05}s">
            <div class="bar-label">${s.name}</div>
            <div class="bar-track">
                <div class="bar-fill blue" style="width: ${(s.count / maxVal) * 100}%">
                    ${s.count > maxVal * 0.15 ? s.count : ""}
                </div>
            </div>
            <div class="bar-value">${formatNumber(s.count)}</div>
        </div>
    `
        )
        .join("");
}

// ── Salary by Title Chart ────────────────────────────────────────────────────

function renderSalaryByTitleChart(salaries) {
    const container = document.getElementById("salary-title-chart");
    const maxVal = Math.max(...salaries.map((s) => s.avg_salary));

    container.innerHTML = salaries
        .slice(0, 12)
        .map(
            (s, i) => `
        <div class="bar-row animate" style="animation-delay: ${i * 0.05}s">
            <div class="bar-label">${s.name}</div>
            <div class="bar-track">
                <div class="bar-fill green" style="width: ${(s.avg_salary / maxVal) * 100}%">
                    $${formatNumber(s.avg_salary)}
                </div>
            </div>
            <div class="bar-value">${s.count} jobs</div>
        </div>
    `
        )
        .join("");
}

// ── Category Donut ───────────────────────────────────────────────────────────

function renderCategoryDonut(categories) {
    const container = document.getElementById("category-donut");
    const total = categories.reduce((sum, c) => sum + c.count, 0);
    const colors = [COLORS.blue, COLORS.green, COLORS.orange, COLORS.purple, COLORS.cyan, COLORS.pink];

    // Build conic gradient
    let gradient = "";
    let cumulative = 0;
    categories.forEach((c, i) => {
        const pct = (c.count / total) * 100;
        gradient += `${colors[i % colors.length]} ${cumulative}% ${cumulative + pct}%`;
        if (i < categories.length - 1) gradient += ", ";
        cumulative += pct;
    });

    const legendHTML = categories
        .map(
            (c, i) => `
        <div class="legend-item">
            <div class="legend-dot" style="background: ${colors[i % colors.length]}"></div>
            <span class="legend-text">${c.name}</span>
            <span class="legend-value">${formatNumber(c.count)}</span>
        </div>
    `
        )
        .join("");

    container.innerHTML = `
        <div class="donut-container">
            <div class="donut-chart" style="background: conic-gradient(${gradient})">
                <div class="donut-center">
                    <div class="num">${formatNumber(total)}</div>
                    <div class="txt">Total Jobs</div>
                </div>
            </div>
            <div class="legend">${legendHTML}</div>
        </div>
    `;
}

// ── Employment Type Donut ────────────────────────────────────────────────────

function renderEmploymentDonut(types) {
    const container = document.getElementById("employment-donut");
    const total = types.reduce((sum, t) => sum + t.count, 0);
    const colors = [COLORS.indigo, COLORS.teal, COLORS.amber, COLORS.rose];

    let gradient = "";
    let cumulative = 0;
    types.forEach((t, i) => {
        const pct = (t.count / total) * 100;
        gradient += `${colors[i % colors.length]} ${cumulative}% ${cumulative + pct}%`;
        if (i < types.length - 1) gradient += ", ";
        cumulative += pct;
    });

    const legendHTML = types
        .map(
            (t, i) => `
        <div class="legend-item">
            <div class="legend-dot" style="background: ${colors[i % colors.length]}"></div>
            <span class="legend-text">${t.name}</span>
            <span class="legend-value">${((t.count / total) * 100).toFixed(1)}%</span>
        </div>
    `
        )
        .join("");

    container.innerHTML = `
        <div class="donut-container">
            <div class="donut-chart" style="background: conic-gradient(${gradient})">
                <div class="donut-center">
                    <div class="num">${types.length}</div>
                    <div class="txt">Types</div>
                </div>
            </div>
            <div class="legend">${legendHTML}</div>
        </div>
    `;
}

// ── Location Table ───────────────────────────────────────────────────────────

function renderLocationTable(locations) {
    const container = document.getElementById("location-table");
    const total = locations.reduce((sum, l) => sum + l.count, 0);

    container.innerHTML = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Location</th>
                    <th>Jobs</th>
                    <th>% of Total</th>
                    <th>Avg Salary</th>
                </tr>
            </thead>
            <tbody>
                ${locations
                    .map(
                        (l) => `
                    <tr>
                        <td>${l.name}</td>
                        <td><span class="count-badge">${formatNumber(l.count)}</span></td>
                        <td>${((l.count / total) * 100).toFixed(1)}%</td>
                        <td class="salary">$${formatNumber(l.avg_salary)}</td>
                    </tr>
                `
                    )
                    .join("")}
            </tbody>
        </table>
    `;
}

// ── Experience Level Chart ───────────────────────────────────────────────────

function renderExperienceChart(experience) {
    const container = document.getElementById("experience-chart");
    const maxVal = Math.max(...experience.map((e) => e.avg_salary));

    container.innerHTML = experience
        .map(
            (e, i) => `
        <div class="bar-row animate" style="animation-delay: ${i * 0.05}s">
            <div class="bar-label">${e.name}</div>
            <div class="bar-track">
                <div class="bar-fill purple" style="width: ${(e.avg_salary / maxVal) * 100}%">
                    $${formatNumber(e.avg_salary)}
                </div>
            </div>
            <div class="bar-value">${formatNumber(e.count)} jobs</div>
        </div>
    `
        )
        .join("");
}

// ── Skills Salary Premium ────────────────────────────────────────────────────

function renderSkillsSalaryChart(skills) {
    const container = document.getElementById("skills-salary-chart");
    const maxVal = Math.max(...skills.map((s) => s.avg_salary));

    container.innerHTML = skills
        .slice(0, 12)
        .map(
            (s, i) => `
        <div class="bar-row animate" style="animation-delay: ${i * 0.05}s">
            <div class="bar-label">${s.name}</div>
            <div class="bar-track">
                <div class="bar-fill orange" style="width: ${(s.avg_salary / maxVal) * 100}%">
                    $${formatNumber(s.avg_salary)}
                </div>
            </div>
            <div class="bar-value">${formatNumber(s.count)} jobs</div>
        </div>
    `
        )
        .join("");
}

// ── Monthly Trends ───────────────────────────────────────────────────────────

function renderMonthlyTrends(trends) {
    const container = document.getElementById("monthly-trends-chart");
    const maxVal = Math.max(...trends.map((t) => t.count));
    const barWidth = 100 / trends.length;

    const barsHTML = trends
        .map(
            (t, i) => `
        <div style="display:flex; flex-direction:column; align-items:center; flex:1; gap:6px;">
            <span style="font-size:0.72rem; color:var(--text-muted)">${formatNumber(t.count)}</span>
            <div style="width:100%; max-width:48px; height:${(t.count / maxVal) * 200}px;
                        background:linear-gradient(180deg, var(--accent), var(--indigo, #6366f1));
                        border-radius:6px 6px 0 0; transition:height 1s ease; min-height:8px;"></div>
            <span style="font-size:0.68rem; color:var(--text-secondary); transform:rotate(-45deg);
                         white-space:nowrap; margin-top:4px;">${t.month}</span>
        </div>
    `
        )
        .join("");

    container.innerHTML = `
        <div style="display:flex; align-items:flex-end; gap:8px; height:280px; padding-bottom:40px;">
            ${barsHTML}
        </div>
    `;
}

// ── Key Insights ─────────────────────────────────────────────────────────────

function renderInsights(d) {
    const container = document.getElementById("insights-grid");
    const topSkill = d.top_skills[0];
    const topPayingSkill = d.skills_salary[0];
    const remotePercent = ((d.overview.remote_jobs / d.overview.total_jobs) * 100).toFixed(1);

    const insights = [
        { title: "Most In-Demand Skill", value: topSkill.name, desc: `Found in ${topSkill.count} job listings` },
        { title: "Highest Paying Skill", value: topPayingSkill.name, desc: `$${formatNumber(topPayingSkill.avg_salary)} average salary` },
        { title: "Remote Work", value: `${remotePercent}%`, desc: `${formatNumber(d.overview.remote_jobs)} remote positions` },
        { title: "Top Category", value: d.jobs_by_category[0].name, desc: `${formatNumber(d.jobs_by_category[0].count)} open positions` },
        { title: "Highest Avg Salary", value: d.salary_by_title[0].name, desc: `$${formatNumber(d.salary_by_title[0].avg_salary)} average` },
        { title: "Entry Level Jobs", value: formatNumber(d.entry_level_jobs.reduce((s, j) => s + j.count, 0)), desc: "Positions available now" },
    ];

    container.innerHTML = insights
        .map(
            (ins, i) => `
        <div class="insight-card animate" style="animation-delay: ${i * 0.08}s">
            <div class="insight-title">${ins.title}</div>
            <div class="insight-value">${ins.value}</div>
            <div class="insight-desc">${ins.desc}</div>
        </div>
    `
        )
        .join("");
}

// ── Entry Level Table ────────────────────────────────────────────────────────

function renderEntryLevelTable(jobs, skills) {
    const jobsContainer = document.getElementById("entry-level-table");
    const skillsContainer = document.getElementById("entry-skills-chart");

    // Jobs table
    jobsContainer.innerHTML = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Job Title</th>
                    <th>Open Positions</th>
                    <th>Avg Salary</th>
                </tr>
            </thead>
            <tbody>
                ${jobs
                    .map(
                        (j) => `
                    <tr>
                        <td>${j.name}</td>
                        <td><span class="count-badge">${formatNumber(j.count)}</span></td>
                        <td class="salary">$${formatNumber(j.avg_salary)}</td>
                    </tr>
                `
                    )
                    .join("")}
            </tbody>
        </table>
    `;

    // Skills chart
    const maxVal = Math.max(...skills.map((s) => s.count));
    skillsContainer.innerHTML = skills
        .map(
            (s, i) => `
        <div class="bar-row animate" style="animation-delay: ${i * 0.05}s">
            <div class="bar-label">${s.name}</div>
            <div class="bar-track">
                <div class="bar-fill green" style="width: ${(s.count / maxVal) * 100}%">
                    ${s.count}
                </div>
            </div>
        </div>
    `
        )
        .join("");
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function formatNumber(num) {
    return Math.round(num).toLocaleString();
}
