-- Biggest absolute drop-off per stage, split by channel
WITH per_channel AS (
  SELECT d.channel, f.stage, COUNT(*) AS users
  FROM fact_funnel f JOIN dim_user d ON d.user_id=f.user_id
  GROUP BY d.channel, f.stage
),
ranked AS (
  SELECT channel, stage, users,
         LAG(users) OVER (PARTITION BY channel ORDER BY CASE stage WHEN 'Visit' THEN 1 WHEN 'Signup' THEN 2
           WHEN 'Activated' THEN 3 WHEN 'Trial Started' THEN 4 WHEN 'Paid' THEN 5 END) AS prev_users
  FROM per_channel
)
SELECT channel, stage, users AS stayed, prev_users AS entered,
       (prev_users - users) AS lost_users,
       ROUND(100.0*(prev_users-users)/prev_users,2) AS drop_pct
FROM ranked WHERE prev_users IS NOT NULL
ORDER BY lost_users DESC LIMIT 10;
