-- Channel value: MRR, paying users, revenue per visitor
SELECT d.channel,
       COUNT(*) AS visitors,
       SUM(CASE WHEN d.mrr>0 THEN 1 ELSE 0 END) AS paying_users,
       SUM(d.mrr) AS mrr_inr,
       ROUND(1.0*SUM(d.mrr)/COUNT(*),2) AS revenue_per_visitor_inr
FROM dim_user d GROUP BY d.channel ORDER BY mrr_inr DESC;
