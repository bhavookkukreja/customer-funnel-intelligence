-- Visit->Paid conversion by acquisition channel
WITH v AS (SELECT channel, COUNT(*) n FROM dim_user GROUP BY channel),
p AS (SELECT channel, COUNT(*) paid FROM dim_user WHERE mrr > 0 GROUP BY channel)
SELECT v.channel, v.n AS visitors, p.paid,
       ROUND(100.0*p.paid/v.n,2) AS visit_to_paid_pct
FROM v JOIN p USING(channel) ORDER BY visit_to_paid_pct DESC;
