# Rabt Network Analytics — Power BI Dashboard

> A Power BI dashboard built on a synthetic dataset modeled after a professional networking platform (LinkedIn-style) in the Saudi market.
> **All data is synthetic** and generated for practice. "Rabt" and all company names are fictional.

## Business Questions
1. Which content formats and topics drive the highest reach and engagement?
2. When is the best time (day / hour) to publish?
3. Which skills are most in demand in job postings, and in which cities?
4. Where do candidates drop off in the hiring funnel?
5. How do salaries vary by experience level and job family?

## Data Model (Star Schema)

| Table | Type | Rows | Key |
|---|---|---|---|
| `DimDate` | Dimension | 669 | `Date` |
| `DimMember` | Dimension | 6,000 | `MemberID` |
| `DimCompany` | Dimension | 120 | `CompanyID` |
| `DimSkill` | Dimension | 20 | `SkillID` |
| `FactPosts` | Fact | 22,000 | `PostID` |
| `FactJobPostings` | Fact | 1,800 | `JobID` |
| `FactApplications` | Fact | 17,087 | `ApplicationID` |
| `BridgeJobSkill` | Bridge | 5,464 | `JobID` + `SkillID` |

**Relationships (all one-to-many, single direction unless noted):**
- `DimDate[Date]` → `FactPosts[PostDate]`, `FactApplications[ApplyDate]`, `FactJobPostings[PostDate]`
- `DimMember[MemberID]` → `FactPosts[MemberID]`, `FactApplications[MemberID]`
- `DimCompany[CompanyID]` → `FactJobPostings[CompanyID]`
- `FactJobPostings[JobID]` → `FactApplications[JobID]`, `BridgeJobSkill[JobID]`
- `DimSkill[SkillID]` → `BridgeJobSkill[SkillID]` (set cross-filter to **Both** on `BridgeJobSkill[JobID]` to filter jobs by skill)

## Report Pages
1. **Overview** — KPI cards, monthly impressions trend, engagement rate, member growth
2. **Content Performance** — Format × Topic matrix, posting-hour heatmap, weekday analysis
3. **Job Market** — Top skills, postings by city, work type, salary by level
4. **Hiring Funnel** — Applied → Viewed → Interview → Offer → Hired, response time, source

## Files
| File | What it is |
|---|---|
| `generate_dataset.py` | Python (NumPy + pandas) script that builds the dataset with realistic patterns: weekday and Ramadan effects, format-based reach, a hiring funnel |
| `measures.dax` | All DAX measures used in the report |
| `Rabt_Professional_Network_Dataset.xlsx` | The generated dataset, one sheet per table |

Rebuild the data: `pip install numpy pandas openpyxl` then `python generate_dataset.py data`.

## Tools
Power BI Desktop · Power Query · DAX · Star schema modeling
