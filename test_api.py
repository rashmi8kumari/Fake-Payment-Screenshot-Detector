import requests

# Flask server ka API URL
url = "http://127.0.0.1:5000/upload"

# Apni image ka path (transaction screenshot)
file_path = "lakshtransaction.jpg"  # Apni image ka actual path daalna

# Image file ko open karke POST request bhejenge
files = {"file": open(file_path, "rb")}
response = requests.post(url, files=files)

# Response status code aur text print karo
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# JSON parse try karo
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("❌ Error: Response is not in JSON format!")

