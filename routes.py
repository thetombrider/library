# routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timedelta
from models import Book, BookBase, Member, MemberBase, Loan, LoanBase
from dependencies import get_supabase
from supabase import Client
from postgrest.exceptions import APIError
from middleware import verify_token

books_router = APIRouter()

@books_router.post("/", response_model=Book)
async def create_book(book: BookBase, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table("books").insert(book.dict()).execute()
        if len(response.data) == 0:
            raise HTTPException(status_code=400, detail="Failed to create book")
        return {**response.data[0]}
    except APIError as e:
        if e.code == '23505' and 'books_isbn_key' in str(e):
            raise HTTPException(status_code=400, detail="A book with this ISBN already exists")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while creating the book")

@books_router.get("/books/", response_model=List[Book])
async def read_books(supabase: Client = Depends(get_supabase), user: dict = Depends(verify_token)):
    response = supabase.table("books").select("*").execute()
    return response.data


@books_router.get("/members/", response_model=List[Member])
async def read_members(supabase: Client = Depends(get_supabase), user: dict = Depends(verify_token)):
    try:
        response = supabase.table("members").select("id", "email", "name").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching members: {str(e)}")

@books_router.post("/loans/", response_model=Loan)
async def create_loan(loan: LoanBase, supabase: Client = Depends(get_supabase), user: dict = Depends(verify_token)):
    book_response = supabase.table("books").select("quantity").eq("id", loan.book_id).execute()
    if len(book_response.data) == 0 or book_response.data[0]['quantity'] <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    loan_date = datetime.utcnow()
    return_date = loan_date + timedelta(days=30)
    loan_data = {
        **loan.dict(),
        "loan_date": loan_date.isoformat(),
        "return_date": return_date.isoformat()
    }
    loan_response = supabase.table("loans").insert(loan_data).execute()
    if len(loan_response.data) == 0:
        raise HTTPException(status_code=400, detail="Failed to create loan")
    
    supabase.table("books").update({"quantity": book_response.data[0]['quantity'] - 1}).eq("id", loan.book_id).execute()
    
    return {**loan_response.data[0]}

@books_router.get("/loans/", response_model=List[Loan])
async def read_loans(supabase: Client = Depends(get_supabase), user: dict = Depends(verify_token)):
    response = supabase.table("loans").select("*").execute()
    return response.data

@books_router.put("/return/{loan_id}", response_model=Loan)
async def return_book(loan_id: int, supabase: Client = Depends(get_supabase), user: dict = Depends(verify_token)):
    loan_response = supabase.table("loans").select("*").eq("id", loan_id).execute()
    if len(loan_response.data) == 0 or loan_response.data[0].get('return_date'):
        raise HTTPException(status_code=400, detail="Invalid loan or book already returned")
    
    return_date = datetime.utcnow().isoformat()
    update_response = supabase.table("loans").update({"return_date": return_date}).eq("id", loan_id).execute()
    
    book_id = loan_response.data[0]['book_id']
    supabase.table("books").update({"quantity": supabase.table("books").select("quantity").eq("id", book_id).execute().data[0]['quantity'] + 1}).eq("id", book_id).execute()
    
    return {**update_response.data[0]}

@books_router.post("/members/", response_model=Member)
async def create_member(member: MemberBase, supabase: Client = Depends(get_supabase), user: dict = Depends(verify_token)):
    try:
        response = supabase.table("members").insert(member.dict()).execute()
        if len(response.data) == 0:
            raise HTTPException(status_code=400, detail="Failed to create member")
        return {**response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the member: {str(e)}")