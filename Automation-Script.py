import os
import json
import requests
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# 🔹 Load Google Cloud credentials
SERVICE_ACCOUNT_FILE = "your-service-account.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# 🔹 BigQuery Details
PROJECT_ID = "your-gcp-project"
DATASET_ID = "sales_reports"
SALES_TABLE = f"{PROJECT_ID}.{DATASET_ID}.monthly_sales"
INSIGHTS_TABLE = f"{PROJECT_ID}.{DATASET_ID}.insights"

# 🔹 Vertex AI API Details
VERTEX_AI_ENDPOINT = "https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/text-bison@001:predict"
TOKEN = "YOUR_ACCESS_TOKEN"

# 🔹 1. Fetch Sales Data from an External API (or CSV)
def fetch_sales_data():
    """Fetches sales data from an external API (or reads from CSV)."""
    try:
        # Example: Fetch from an API
        url = "https://api.example.com/sales-data"
        response = requests.get(url)
        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data["sales"])
        
        # If using CSV instead:
        # df = pd.read_csv("sales_data.csv")

        print(f"✅ {len(df)} records fetched.")
        return df
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

# 🔹 2. Load Data into BigQuery
def upload_to_bigquery(df, table_id):
    """Uploads DataFrame to BigQuery."""
    try:
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        job = client.load_table_from_dataframe(df, table_id)
        job.result()  # Wait for completion
        print(f"✅ Data uploaded to {table_id}")
    except Exception as e:
        print(f"❌ Error uploading to BigQuery: {e}")

# 🔹 3. Generate Insights Using Vertex AI
def generate_sales_insights():
    """Calls Vertex AI API to analyze sales trends."""
    try:
        payload = {
            "instances": [
                {"prompt": "Analyze the latest sales data trends and provide key insights."}
            ]
        }
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(VERTEX_AI_ENDPOINT, json=payload, headers=headers)
        insights = response.json()

        print(f"✅ Insights generated: {insights}")
        return insights["predictions"][0]
    except Exception as e:
        print(f"❌ Error generating insights: {e}")
        return None

# 🔹 4. Store AI Insights in BigQuery
def save_insights_to_bigquery(insight_text):
    """Saves Vertex AI insights to BigQuery."""
    try:
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        rows = [{"date": datetime.today().strftime("%Y-%m-%d"), "insight": insight_text}]
        errors = client.insert_rows_json(INSIGHTS_TABLE, rows)
        
        if errors:
            print(f"❌ BigQuery Error: {errors}")
        else:
            print("✅ AI Insights saved to BigQuery")
    except Exception as e:
        print(f"❌ Error saving insights: {e}")

# 🔹 5. Automate Looker Studio Refresh (Google Sheets as Data Source)
def trigger_looker_refresh(sheet_url):
    """Triggers Looker Studio refresh via Google Sheets API."""
    try:
        requests.post(sheet_url)
        print("✅ Looker Studio Refresh Triggered")
    except Exception as e:
        print(f"❌ Error triggering Looker Studio refresh: {e}")

# 🔹 Main Function (Scheduler Ready)
def main():
    print("🚀 Automation Started")
    
    # Step 1: Fetch Data
    df = fetch_sales_data()
    if df is not None:
        df["date"] = pd.to_datetime(df["date"]).dt.date  # Ensure date format
        upload_to_bigquery(df, SALES_TABLE)

    # Step 2: Generate Insights
    insight_text = generate_sales_insights()
    if insight_text:
        save_insights_to_bigquery(insight_text)

    # Step 3: Refresh Looker Studio
    LOOKER_SHEET_URL = "https://docs.google.com/spreadsheets/d/your-sheet-id/gviz/tq?tqx=out:csv"
    trigger_looker_refresh(LOOKER_SHEET_URL)

    print("🎉 Automation Completed")

# Run the script
if __name__ == "__main__":
    main()
