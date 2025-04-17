# Databricks notebook source
dbutils.library.restartPython()

# COMMAND ----------

import mlflow.pyfunc

class capitalize(mlflow.pyfunc.PythonModel):
    def __init__(self, input_string):
        import requests
        self.input_string = input_string

    def predict(self, context, model_input, params=None):
        return str(model_input).upper()

# COMMAND ----------

capitalize_model = capitalize(input_string="hello world")

with mlflow.start_run():
    mlflow.pyfunc.log_model("lg_capitalize", 
                            python_model=capitalize_model)

# COMMAND ----------

import mlflow.pyfunc

loaded_model = mlflow.pyfunc.load_model(f"runs:/e504b86a9f094d8bb22458ff5bb7a5a7/lg_capitalize")    

loaded_model.predict("hello world!")

# COMMAND ----------

import json
import os
import requests

url = 'https://workspace-url/serving-endpoints/lg_capitalize/invocations'
databricks_token = mlflow.utils.databricks_utils.get_databricks_host_creds().token

headers = {'Authorization': f'Bearer {databricks_token}', 'Content-Type': 'application/json'}

data = {
  "inputs": "this is a test"
}
data_json = json.dumps(data, allow_nan=True)

response = requests.request(method='POST', headers=headers, url=url, data=data_json)
if response.status_code != 200:
  raise Exception(f'Request failed with status {response.status_code}, {response.text}')

print(response.json()['predictions'])

# COMMAND ----------


