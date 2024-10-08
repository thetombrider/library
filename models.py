# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    quantity: int

class Book(BookBase):
    id: int

class MemberBase(BaseModel):
    email: str
    name: str

class Member(MemberBase):
    id: str

class LoanBase(BaseModel):
    book_id: int
    member_id: int

class Loan(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None