import requests
import json
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

# API endpoint URL (replace with your actual deployed API URL)
url = os.getenv("RENDER_URL")  # Default to localhost if not set

# Signup credentials
signup_data = {
    "credentials": {
        "email": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    },
    "profile": {
        "full_name": "Tommy"
    }
}

# Login credentials
credentials = {
    "email": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD")
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

# Headers for authenticated requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Get existing members
members_response = requests.get(f"{url}/books/members/", headers=headers)

if members_response.status_code == 200:
    print("Members retrieved successfully!")
    members = members_response.json()
    if members:
        member_id = members[0]["id"]
        print("Using Member ID:", member_id)
    else:
        print("No members found. Please sign up a new user first.")
        exit(1)
else:
    print("Failed to retrieve members.")
    print("Status code:", members_response.status_code)
    print("Response:", members_response.text)
    exit(1)

# Generate a unique ISBN
isbn = f"9780{random.randint(10, 99)}{random.randint(100000, 999999)}{random.randint(0, 9)}"

# Book data
new_book = {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": isbn,
    "quantity": 5
}

# Add a new book
book_response = requests.post(f"{url}/books/", json=new_book, headers=headers)

if book_response.status_code == 200:
    print("Book added successfully!")
    book_id = book_response.json()["id"]
    print("Book ID:", book_id)
else:
    print("Failed to add book.")
    print("Status code:", book_response.status_code)
    print("Response:", book_response.text)
    exit(1)

# Create a new loan
new_loan = {
    "book_id": book_id,
    "member_id": member_id
}

loan_response = requests.post(f"{url}/books/loans/", json=new_loan, headers=headers)

if loan_response.status_code == 200:
    print("Loan created successfully!")
    print("Response:", json.dumps(loan_response.json(), indent=2))
else:
    print("Failed to create loan.")
    print("Status code:", loan_response.status_code)
    print("Response:", loan_response.text)
