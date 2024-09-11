import requests
import json
from dotenv import load_dotenv
import os
import random

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

# Headers for authenticated requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Create a new member
new_member = {
    "name": "John Doe",
    "email": f"john.doe{random.randint(1, 1000)}@example.com"
}

member_response = requests.post(f"{url}/books/members/", json=new_member, headers=headers)

if member_response.status_code == 200:
    print("Member added successfully!")
    member_id = member_response.json()["id"]
    print("Member ID:", member_id)
else:
    print("Failed to add member.")
    print("Status code:", member_response.status_code)
    print("Response:", member_response.text)
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
