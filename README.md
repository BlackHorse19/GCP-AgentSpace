# 🚀 Sales Report Automation with Google Vertex AI & Looker Studio

## **📌 Overview**
This project automates sales report processing using **Google Vertex AI, BigQuery, and Looker Studio**. The system fetches sales data, processes it using AI, stores insights in BigQuery, and updates Looker Studio dashboards automatically.

---

## **🛠️ Features**
✅ **Fetches sales data** from an API or CSV file
✅ **Stores data** in Google BigQuery
✅ **Uses Vertex AI** to analyze trends and generate insights
✅ **Saves AI-generated insights** to BigQuery
✅ **Updates Looker Studio dashboards** automatically
✅ **Runs daily** using Google Cloud Scheduler

---

## **📂 Project Structure**
```
📦 sales-report-automation
 ├── sales_pipeline.py      # Main automation script
 ├── README.md              # Project documentation
 ├── service-account.json   # Google Cloud service account credentials
 ├── requirements.txt       # Python dependencies
```

---

## **🔧 Setup & Installation**

### **1️⃣ Prerequisites**
- Google Cloud Platform (GCP) account
- **Enabled APIs**:
  - Vertex AI
  - BigQuery
  - Cloud Functions
- Installed **Python 3.10+** and the following libraries:
  ```sh
  pip install google-cloud-bigquery google-cloud-storage google-auth requests pandas
  ```

### **2️⃣ Configure Google Cloud Credentials**
1. Create a **Service Account** in Google Cloud.
2. Assign **BigQuery Admin & Vertex AI User** roles.
3. Download the `service-account.json` file and save it in the project folder.
4. Set environment variable:
   ```sh
   export GOOGLE_APPLICATION_CREDENTIALS="service-account.json"
   ```

### **3️⃣ Deploy Cloud Function**
```sh
gcloud functions deploy sales_pipeline --runtime python310 --trigger-http --allow-unauthenticated
```

### **4️⃣ Schedule Automation with Cloud Scheduler**
```sh
gcloud scheduler jobs create http daily_sales_job \
  --schedule "0 9 * * *" \
  --uri "https://YOUR_CLOUD_FUNCTION_URL" \
  --http-method GET
```

---

## **🚀 How It Works**
1️⃣ **Fetches Sales Data** → From API or CSV file  
2️⃣ **Stores Data in BigQuery** → Table: `sales_reports.monthly_sales`  
3️⃣ **Processes Data with AI** → Vertex AI generates insights  
4️⃣ **Stores Insights in BigQuery** → Table: `sales_reports.insights`  
5️⃣ **Updates Looker Studio Dashboard** → Sales reports refresh automatically 🎉  

---

## **📊 Looker Studio Dashboard**
To visualize the reports:
1. Go to [Looker Studio](https://lookerstudio.google.com/)
2. Add **BigQuery as a data source**
3. Create charts and tables using `monthly_sales` and `insights`
4. Apply **filters** for date and region

---

## **📬 Want Daily Reports?**
You can add an **email notification** using Google Cloud Functions to receive AI-generated insights **every morning**! ☀️

Need help? Feel free to ask! 😊🚀

