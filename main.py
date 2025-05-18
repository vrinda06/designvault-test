import os
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from scraper import search_serpapi_inspo

load_dotenv()

# --- Google Sheet Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds_json = os.getenv("GCP_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("et__Prime_Design Vault").sheet1

# --- Flask App Setup ---
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ DesignVaultGPT is live!"

@app.route("/query")
def query_sheet():
    user_query = request.args.get("ask", "").lower()
    data = sheet.get_all_records()
    matched_rows = []

    for row in data:
        row_text = " ".join([str(value).lower() for value in row.values()])
        if all(word in row_text for word in user_query.split()):
            matched_rows.append(row)

    if not matched_rows:
        return jsonify([{"note": "❌ I couldn’t find anything in the campaign vault for that."}])

    return jsonify(matched_rows)

@app.route("/generate-inspo")
def generate_inspo():
    user_query = request.args.get("ask", "").lower()
    data = sheet.get_all_records()
    matched_rows = []

    for row in data:
        row_text = " ".join([str(value).lower() for value in row.values()])
        if all(word in row_text for word in user_query.split()):
            matched_rows.append(row)

    if not matched_rows:
        return jsonify([{"note": "❌ No inspiration found in the design vault for that term."}])

    motifs = ", ".join({row.get("Motifs Used", "") for row in matched_rows})
    hooks = ", ".join({row.get("Creative Hook", "") for row in matched_rows})
    objectives = ", ".join({row.get("Objective", "") for row in matched_rows})
    notes = ". ".join({row.get("Design Notes", "") for row in matched_rows})

    prompt = f"""
    Based on past campaigns with the objective: {objectives},
    and motifs such as {motifs},
    and creative hooks like: {hooks},

    suggest a new design layout for a campaign titled: {user_query.title()}.

    Include:
    - Layout structure
    - Font + Color recommendations
    - CTA and headline copy
    - Any animation or visual style ideas

    Past design notes to consider: {notes}
    """

    return jsonify({"prompt": prompt})

@app.route("/test-freepik")
def test_freepik():
    keyword = request.args.get("ask", "holi sale banner")
    results = search_serpapi_inspo(keyword)
    return jsonify(results)

# --- ✅ Railway-compatible server launch ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
