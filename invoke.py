import requests

# Endpoint URL
url = "http://localhost:8090/v2/models/iris_clf/infer"

sample_input = [[5.1, 3.5, 1.4, 0.2]]

# Constructing the payload
payload = {
    "inputs": sample_input
}

# Make a POST request
response = requests.post(url, json=payload)

# Checking response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.text)
