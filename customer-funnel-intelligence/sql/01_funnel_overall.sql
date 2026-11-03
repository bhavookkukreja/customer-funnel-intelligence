-- Stage counts, stage-to-stage conversion and cumulative conversion
WITH counts AS (
  SELECT stage, COUNT(*) AS users FROM fact_funnel GROUP BY stage
),
ordered AS (
  SELECT stage, users,
         LAG(users) OVER (ORDER BY CASE stage WHEN 'Visit' THEN 1 WHEN 'Signup' THEN 2
           WHEN 'Activated' THEN 3 WHEN 'Trial Started' THEN 4 WHEN 'Paid' THEN 5 END) AS prev_users
  FROM counts
)
SELECT stage, users,
       ROUND(100.0*users/prev_users, 2) AS step_conversion_pct,
       ROUND(100.0*users/(SELECT users FROM counts WHERE stage='Visit'), 2) AS cum_conversion_pct
FROM ordered ORDER BY CASE stage WHEN 'Visit' THEN 1 WHEN 'Signup' THEN 2
  WHEN 'Activated' THEN 3 WHEN 'Trial Started' THEN 4 WHEN 'Paid' THEN 5 END;
