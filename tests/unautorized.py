import requests
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# API endpoint URL
url = os.getenv("RENDER_URL")

# Generate a random book_id and member_id
book_id = random.randint(1, 100)
member_id = random.randint(1, 100)

# Loan data
loan_data = {
    "book_id": book_id,
    "member_id": member_id
}

# Send POST request to create a loan
response = requests.post(f"{url}/books/loans/", json=loan_data)

# Print the response
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")
