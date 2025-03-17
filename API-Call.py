import requests

vertex_ai_endpoint = "https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/text-bison@001:predict"
headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
data = {"instances": [{"prompt": "Analyze last month's sales trends"}]}

response = requests.post(vertex_ai_endpoint, json=data, headers=headers)
print(response.json())
