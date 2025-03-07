# Create the BigQuery dataset and table by running the following in Cloud Shell:

# bq --location=US mk -d users
# bq mk -t users.favorite_flavors favorite_flavors_schema.json

# In your Cloud Shell terminal, paste the following to create a favorite_flavors_schema.json file to define the schema for a BigQuery table which will be used to record users' favorite flavorss:

cat > favorite_flavors_schema.json << EOF
[
  {
    "name": "email",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "favorite_flavor",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

https://record-favorite-flavor-5878556456.us-central1.run.app


# From the options at the top of the Cloud Run console, select Write a Function.:
# Click the requirements.txt file on the left, delete its contents, and paste in the following:

# functions-framework==3.*
# google-cloud-bigquery

# Click the main.py file on the left, delete its contents, and paste in the following code. This function will take the travel request details provided to a POST request as JSON and write those values to a new row in the BigQuery table you created earlier:

import functions_framework
from google.cloud import bigquery

@functions_framework.http
def record_favorite_flavor(request):
    """Writes user emails and favorite flavors to BigQuery."""

    request_json = request.get_json(silent=True)
    request_args = request.args
    print("JSON:" + str(request_json))
    print("args:" + str(request_args))

    bq_client = bigquery.Client()
    table_id = "YOUR_PROJECT_ID.users.favorite_flavors"

    row_to_insert = [
        {"email": request_json["email"],
        "favorite_flavor": request_json["favorite_flavor"]
        },
    ]

    errors = bq_client.insert_rows_json(table_id, row_to_insert)  # Make an API request.
    if errors == []:
        return {"message": "New row has been added."}
    else:
        return {"message": "Encountered errors while inserting rows: {}".format(errors)}


# For Schema, keep the type YAML selected, and paste the following into the text box. This OpenAPI spec describes an API with:
# a server url set to call your Cloud Run function
# a default path for your Cloud Run function (/) that accepts POST requests that include JSON using a schema called FavoriteFlavor
# a definition of that FavoriteFlavor schema to include the fields you defined in your BigQuery schema at the start of this lab:

openapi: 3.0.0
info:
  title: Favorite Flavors API
  version: 1.0.0
servers:
  - url: 'YOUR_CLOUD_RUN_FUNCTION_URL'
paths:
  /:
    post:
      summary: Record a user's favorite flavor
      operationId: recordFavoriteFlavor
      requestBody:
        description: Favorite flavor to add
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FavoriteFlavor'
      responses:
        '200':
          description: Success
components:
  schemas:
    FavoriteFlavor:
      type: object
      properties:
        email:
          type: string
        favorite_flavor:
          type: string
