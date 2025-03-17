from google.cloud import bigquery

client = bigquery.Client()
table_id = "your_project.your_dataset.sales_data"

rows_to_insert = [
    {"date": "2025-03-16", "sales": 10000, "region": "US"},
    {"date": "2025-03-16", "sales": 8000, "region": "EU"},
]

errors = client.insert_rows_json(table_id, rows_to_insert)
if errors:
    print("Errors:", errors)
else:
    print("Data successfully inserted.")
