import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API endpoint URL (replace with your actual deployed API URL)
url = os.getenv("RENDER_URL")  # Default to localhost if not set

# Login credentials
credentials = {
    "email": "tommasominuto@gmail.com",  # Replace with actual librarian email
    "password": "2000tommy"  # Replace with actual password
}

# Sign in to get the access token
signin_response = requests.post(f"{url}/auth/signin", json=credentials)

if signin_response.status_code == 200:
    access_token = signin_response.json()["access_token"]
    print("Sign in successful!")
else:
    print("Sign in failed.")
    print("Status code:", signin_response.status_code)
    print("Response:", signin_response.text)
    exit(1)

# Book data
new_book = {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "quantity": 5
}

# Send POST request with authentication
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
response = requests.post(f"{url}/books/books", json=new_book, headers=headers)

# Check the response
if response.status_code == 200:
    print("Book added successfully!")
    print("Response:", json.dumps(response.json(), indent=2))
else:
    print("Failed to add book.")
    print("Status code:", response.status_code)
    print("Response:", response.text)
