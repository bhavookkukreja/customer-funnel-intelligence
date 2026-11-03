-- Weekly signup cohort -> % paid (cumulative, weeks 0-4 after signup)
WITH s AS (
  SELECT u.user_id, u.signup_week, MIN(f.event_ts) AS signup_ts
  FROM dim_user u JOIN fact_funnel f ON f.user_id=u.user_id AND f.stage='Signup'
  GROUP BY u.user_id, u.signup_week
),
paid AS (
  SELECT u.user_id, MIN(f.event_ts) AS paid_ts
  FROM dim_user u JOIN fact_funnel f ON f.user_id=u.user_id AND f.stage='Paid'
  GROUP BY u.user_id
)
SELECT s.signup_week,
       COUNT(*) AS cohort_size,
       ROUND(100.0*SUM(CASE WHEN p.paid_ts IS NOT NULL AND
         CAST((julianday(p.paid_ts)-julianday(s.signup_ts))/7 AS INT) <= 0 THEN 1 ELSE 0 END)/COUNT(*),1) AS w0_paid_pct,
       ROUND(100.0*SUM(CASE WHEN p.paid_ts IS NOT NULL AND
         CAST((julianday(p.paid_ts)-julianday(s.signup_ts))/7 AS INT) <= 1 THEN 1 ELSE 0 END)/COUNT(*),1) AS w1_paid_pct,
       ROUND(100.0*SUM(CASE WHEN p.paid_ts IS NOT NULL AND
         CAST((julianday(p.paid_ts)-julianday(s.signup_ts))/7 AS INT) <= 2 THEN 1 ELSE 0 END)/COUNT(*),1) AS w2_paid_pct
FROM s LEFT JOIN paid p ON p.user_id=s.user_id
GROUP BY s.signup_week ORDER BY s.signup_week;
