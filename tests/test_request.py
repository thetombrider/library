import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API endpoint URL (replace with your actual deployed API URL)
url = os.getenv("RENDER_URL")  # Default to localhost if not set

# Book data
new_book = {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "quantity": 5
}

# Send POST request
response = requests.post(f"{url}/books/", json=new_book)

# Check the response
if response.status_code == 200:
    print("Book added successfully!")
    print("Response:", json.dumps(response.json(), indent=2))
else:
    print("Failed to add book.")
    print("Status code:", response.status_code)
    print("Response:", response.text)
