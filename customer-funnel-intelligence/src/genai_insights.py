"""GenAI insight layer — turns funnel metrics into an executive narrative.
Usage:  python src/genai_insights.py
If OPENAI_API_KEY (any OpenAI-compatible endpoint) is set, calls an LLM.
Otherwise falls back to a deterministic rule-based insight engine (offline)."""
import json, os, datetime

def build_prompt(m):
    return f"""You are a senior growth analyst at WisprPro, an AI voice-dictation SaaS.
Analyze this funnel JSON and write an executive summary (max 200 words) with:
1) headline health assessment, 2) the single biggest leak and its likely cause,
3) two prioritized, specific recommendations, 4) channel budget guidance.
Metrics: {json.dumps(m)}"""

def call_llm(prompt):
    try:
        from openai import OpenAI
        client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
        r = client.chat.completions.create(model=os.getenv("LLM_MODEL","gpt-4o-mini"),
              messages=[{"role":"system","content":"You are a concise growth analyst."},
                        {"role":"user","content":prompt}], temperature=0.3)
        return r.choices[0].message.content, "llm"
    except Exception:
        return None, "failed"

def local_insights(m):
    sc = m["step_conversion_pct"]
    lines = [
      f"Overall visit→paid conversion is {m['overall_visit_to_paid_pct']}% "
      f"({m['paid']} paying users, ₹{m['mrr_inr']:,} MRR) across {m['visitors']:,} visitors.",
      f"Biggest leak: Visit→Signup loses {m['biggest_dropoff']['lost_users']:,} users "
      f"({100-sc['Visit→Signup']:.1f}% fail to sign up). {m['biggest_dropoff']['best_channel']} converts "
      f"best here; {m['biggest_dropoff']['worst_channel']} is the weakest channel.",
      f"Activation (Signup→Activated) is healthy at {sc['Signup→Activated']}%, but "
      f"Activated→Trial ({sc['Activated→Trial Started']}%) and Trial→Paid ({sc['Trial Started→Paid']}%) are the "
      f"monetisation bottlenecks.",
      f"Recommendation 1: add an in-product 'first dictation in 60 seconds' checklist + email nudge to lift activation→trial.",
      f"Recommendation 2: reallocate ~15% of Instagram/Google Ads spend to Referral and LinkedIn "
      f"(rev/visitor ₹{m['channel_rev_per_visitor_inr'].get('Referral')} and ₹{m['channel_rev_per_visitor_inr'].get('LinkedIn')} vs ₹{m['channel_rev_per_visitor_inr'].get('Instagram')}).",
    ]
    return "\n".join(lines), "rule-based"

def main():
    m = json.load(open("reports/funnel_metrics.json"))
    prompt = build_prompt(m)
    if os.getenv("OPENAI_API_KEY"):
        text, src = call_llm(prompt)
        if text is None: text, src = local_insights(m)
    else:
        text, src = local_insights(m)
    out = f"# AI-Generated Funnel Insights\n\n_Source: {src} · {datetime.date.today()}_\n\n{text}\n"
    open("reports/ai_insights.md","w").write(out)
    print(out)

if __name__ == "__main__":
    main()
