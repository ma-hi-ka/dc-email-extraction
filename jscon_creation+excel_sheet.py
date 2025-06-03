import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError
from company_snapshots import CompanySnapshot

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_snapshot_from_text(raw_text: str, source: str = "Unknown Source") -> CompanySnapshot:
    system_prompt = (
        "You are an expert data analyst, greatly skilled in extracting meaningful "
        "and relevant insights from email updates and investment memos. Only return accurate values. "
        "Do not make things up. Leave fields blank if you're not confident. Avoid duplication across fields. "
        "Use the schema provided. Interpret intelligently—e.g. if the word 'clinic' is used instead of 'office', "
        "treat it the same. And most importantly, for every dollar figure, output the full integer value plus one decimal place "
        "– e.g. if the email says $96,282, produce 96282.0. Do not convert dollars into ‘thousands."
    )

    user_prompt = f"""
You are given an investor update email extract or PDF text. Extract all available business metrics and return them as a single structured JSON object. 
For rates/percentages, return the percentage value as it is without the '%' symbol.

JSON SCHEMA FORMAT (use this structure):

{{
  "company_name": "string",
  "year": integer,
  "quarter": integer,
  "industry": "string or null",
  "region": "string or null",
  "financials": {{
    "mrr": float or null,
    "arr": float or null,
    "revenue": float or null,
    "burn_rate": float or null,
    "cash_on_hand": float or null,
    "runway": float or null,
    "gross_margin": float or null
  }},
  "customers": {{
    "active_customers": integer or null,
    "churn_rate": float or null,
    "new_customers": integer or null,
    "usage_stats": "string or null"
  }},
  "sales": {{
    "mom_revenue_growth": float or null,
    "yoy_revenue_growth": float or null,
    "backlog_revenue": float or null,
    "target_revenue": float or null
  }},
  "team": {{
    "team_size": integer or null,
    "new_hires": ["string", ...] or null,
    "required_hires": ["string", ...] or null,
    "operation_notes": "string or null"
  }},
  "company_lowlights": [
    {{
      "description": "string",
      "impact": "string",
      "possible_causes": ["string", ...] or null,
      "future_changes": "string or null"
    }}
  ],
  "fundraising": [
    {{
      "round_type": "string or null",
      "amount_raised": float or null,
      "amount_remaining": float or null,
      "strategic_investors": ["string", ...] or null,
      "advisors": ["string", ...] or null
    }}
  ],
  "product_updates": [
    {{
      "description": "string",
      "event_type": "Launch" | "Upgrade" | "Integration" | "Partnership" | "Churn" | "Hiring",
      "integrations": ["string", ...] or null,
      "impact": "string or null"
    }}
  ],
  "events": [
    {{
      "event_type": "string",
      "description": "string"
    }}
  ],
  "notes": "Any other free-text insights or updates",
  "source": "{source}"
}}

--- START UPDATE TEXT ---
{raw_text}
--- END UPDATE TEXT ---
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    response_text = response.choices[0].message.content

    try:
        response_dict = json.loads(response_text)
        snapshot = CompanySnapshot.parse_obj(response_dict)

        safe_name = snapshot.company_name.replace(" ", "_").replace("/", "_")
        filename = f"{safe_name}_Q{snapshot.quarter}_{snapshot.year}.json"
        os.makedirs("json_schemas", exist_ok=True)
        out_path = os.path.join("json_schemas", filename)

        with open(out_path, "w") as f:
            flat_dict_for_saving = snapshot.model_dump()
            json.dump(flat_dict_for_saving, f, indent=2)

        print(f"✅ Saved JSON schema to {out_path}")
        return snapshot

    except (json.JSONDecodeError, ValidationError) as e:
        print("❌ Failed to parse model:", e)
        with open("failed_gpt_output.json", "w") as f:
            f.write(response_text)
        raise

def flatten_snapshot(snapshot: CompanySnapshot) -> dict:
    flat = {
        "company_name": snapshot.company_name,
        "year": snapshot.year,
        "quarter": snapshot.quarter,
        "industry": snapshot.industry,
        "region": snapshot.region,
    }

    # ───────────<financials>───────────
    if snapshot.financials:
        fin = snapshot.financials.model_dump(exclude_none=True)
        flat["mrr"] = fin.get("mrr")
        flat["arr"] = fin.get("arr")
        flat["revenue"] = fin.get("revenue")
        flat["burn_rate"] = fin.get("burn_rate")
        flat["cash_on_hand"] = fin.get("cash_on_hand")
        flat["runway"] = fin.get("runway")
        flat["gross_margin"] = fin.get("gross_margin")
    else:
        flat.update({
            "mrr": None, "arr": None, "revenue": None,
            "burn_rate": None, "cash_on_hand": None,
            "runway": None, "gross_margin": None
        })

    # ───────────<customers>───────────
    if snapshot.customers:
        cust = snapshot.customers.model_dump(exclude_none=True)
        flat["active_customers"] = cust.get("active_customers")
        flat["churn_rate"] = cust.get("churn_rate")
        flat["new_customers"] = cust.get("new_customers")
        flat["usage_stats"] = cust.get("usage_stats")
    else:
        flat.update({
            "active_customers": None,
            "churn_rate": None,
            "new_customers": None,
            "usage_stats": None
        })

    # ───────────<sales>───────────
    if snapshot.sales:
        s = snapshot.sales.model_dump(exclude_none=True)
        flat["mom_revenue_growth"] = s.get("mom_revenue_growth")
        flat["yoy_revenue_growth"] = s.get("yoy_revenue_growth")
        flat["backlog_revenue"] = s.get("backlog_revenue")
        flat["target_revenue"] = s.get("target_revenue")
    else:
        flat.update({
            "mom_revenue_growth": None,
            "yoy_revenue_growth": None,
            "backlog_revenue": None,
            "target_revenue": None
        })

    # ───────────<team and operations>───────────
    if snapshot.team:
        t = snapshot.team.model_dump(exclude_none=True)
        flat["team_size"] = t.get("team_size")
        flat["new_hires"]      = ", ".join(t.get("new_hires", [])) if t.get("new_hires") else None
        flat["required_hires"] = ", ".join(t.get("required_hires", [])) if t.get("required_hires") else None
        flat["operation_notes"] = t.get("operation_notes")
    else:
        flat.update({
            "team_size": None,
            "new_hires": None,
            "required_hires": None,
            "operation_notes": None
        })

    flat["fundraising"]       = snapshot.fundraising or []
    flat["product_updates"]   = snapshot.product_updates or []
    flat["events"]            = snapshot.events or []
    flat["company_lowlights"] = snapshot.company_lowlights or []

    # ───────────<notes and source>───────────
    flat["notes"]  = snapshot.notes
    flat["source"] = snapshot.source

    for key, value in flat.items():
        if isinstance(value, (int, float)):
            flat[key] = round(float(value), 1)
    return flat


def append_snapshot_to_excel(
    snapshot: CompanySnapshot,
    file_path: str = "/Users/mahika/Desktop/decacorn/email_extraction/investor_updates.xlsx" #change this to wherever the folder is where you want to save the excel sheet.
):
    flat_dict = flatten_snapshot(snapshot)
    new_df = pd.DataFrame([flat_dict])

    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)

        #error catching: if it accidentally creates a top-level “financials” or “customers” columns, we need to drop them:
        nested_cols = [c for c in existing_df.columns
                       if c in ("financials", "customers", "sales", "team",
                                "fundraising", "product_updates", "events", "company_lowlights")]
        if nested_cols:
            existing_df = existing_df.drop(columns=nested_cols)

        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df.to_excel(file_path, index=False)
    print(f"✅ Snapshot appended to {file_path}")


# –––––––––––<input email update/text here: >–––––––––
if __name__ == "__main__":
    raw_email_text = """
    """

    source = "" #input the source here
    snapshot = generate_snapshot_from_text(raw_email_text, source)
    append_snapshot_to_excel(snapshot)