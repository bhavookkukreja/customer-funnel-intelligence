# Power BI Dashboard Build Guide

## 1. Data model (star schema)
- **fact_funnel** (user_id, stage, stage_order, event_ts) — one row per user per reached stage
- **dim_user** (user_id, channel, device, persona, country, plan, mrr, retained_flag, first_visit_date, signup_week)
- **dim_date** — marked as date table, related to fact_funnel[event_ts]

Get Data → Text/CSV (or SQLite via ODBC) → load `data/processed/*.csv`.

## 2. Core DAX measures
```dax
Users (Stage) = CALCULATE(DISTINCTCOUNT(fact_funnel[user_id]), fact_funnel[stage] = "Visit")

Step Conversion % =
DIVIDE(
    CALCULATE(DISTINCTCOUNT(fact_funnel[user_id]), fact_funnel[stage] = "Paid"),
    CALCULATE(DISTINCTCOUNT(fact_funnel[user_id]), fact_funnel[stage] = "Trial Started")
)

Overall Conv % = DIVIDE([Users Paid], [Users Visit])

MRR = SUM(dim_user[mrr])

Rev / Visitor = DIVIDE([MRR], [Users Visit])
```

## 3. Report pages
1. **Executive Overview** — KPI cards (Visits, Signups, Activation %, Paid, MRR), funnel visual, AI-insight text panel fed from `reports/ai_insights.md`
2. **Channel Deep-Dive** — channel × step-conversion matrix, MRR & rev/visitor bars, slicers (device, persona, date)
3. **Cohorts** — weekly signup cohort triangle (% paid W0-W2) as a matrix with conditional formatting
4. **Drop-off** — waterfall of lost users by stage, top-lost channel table

## 4. Design tips
- Theme: dark header band, accent #4C78A8; consistent number formats (thousands separator, % with 1 dp)
- Drill-through from channel → user-level funnel; tooltip pages on the funnel
- Publish to Power BI Service, set scheduled refresh if swapping to a live source
