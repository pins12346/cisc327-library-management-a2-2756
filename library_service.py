"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_db_connection, get_patron_borrowed_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    TODO: Implement R4 as per requirements
    """
    #Validate the patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."

    #Check if the book exists
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."

    #Check if the patron has borrowed the specific book 
    borrowed_books = get_patron_borrowed_books(patron_id)
    borrowed_record = next((b for b in borrowed_books if b['book_id'] == book_id), None)
    if not borrowed_record:
        return False, f'You have not borrowed "{book["title"]}".'

    #Calculate the late fee by calling the function we implemented 
    late_fee_info = calculate_late_fee_for_book(patron_id, book_id)
    fee_amount = late_fee_info.get('fee_amount', 0.0)

    #Update the record 
    today = datetime.now()
    success_record = update_borrow_record_return_date(patron_id, book_id, today)
    success_availability = update_book_availability(book_id, 1)
    if not success_record or not success_availability:
        return False, "Database error occurred while processing return."
    msg = f'Successfully returned "{book["title"]}".'
    if fee_amount > 0:
        msg += f' Late fee: ${fee_amount:.2f}.'

    return True, msg

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 
    
    
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """
    #Validate the patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {"fee_amount": 0.0, "days_overdue": 0, "status": "Invalid patron ID."}

    #Cehck if the book exists
    book = get_book_by_id(book_id)
    if not book:
        return {"fee_amount": 0.0, "days_overdue": 0, "status": "Book not found."}
    borrowed_books = get_patron_borrowed_books(patron_id)
    borrowed_record = next((b for b in borrowed_books if b['book_id'] == book_id), None)
    if not borrowed_record:
        return {"fee_amount": 0.0, "days_overdue": 0, "status": "Book not currently borrowed by patron."}

    #Calculate the late fee
    today = datetime.now()
    days_overdue = max((today - borrowed_record['due_date']).days, 0)
    fee_amount = 0.0
    if days_overdue > 0:
        first_7_days = min(days_overdue, 7)
        remaining_days = max(days_overdue - 7, 0)
        fee_amount = first_7_days * 0.5 + remaining_days * 1.0
        fee_amount = min(fee_amount, 15.0)

    return {"fee_amount": round(fee_amount, 2), "days_overdue": days_overdue, "status": "Success"}
    

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    
    TODO: Implement R6 as per requirements
    """
    #Making sure the search term is case insensitive 
    search_term = search_term.strip().lower()
    books = []
    #Search logic 
    all_books = get_all_books()
    for book in all_books:
        if search_type == "title" and search_term in book['title'].lower():
            books.append(book)
        elif search_type == "author" and search_term in book['author'].lower():
            books.append(book)
        elif search_type == "isbn" and search_term == book['isbn']:
            books.append(book)

    return books

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """
    #Validate the patron id 
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {"error": "Invalid patron ID."}
    
    #Get the list of currently borrowed books
    borrowed_books = get_patron_borrowed_books(patron_id)
    total_late_fees = 0.0

    books_info = []
    for book in borrowed_books:
        late_fee_info = calculate_late_fee_for_book(patron_id, book['book_id'])
        fee_amount = late_fee_info.get('fee_amount', 0.0)
        days_overdue = late_fee_info.get('days_overdue', 0)
        total_late_fees += fee_amount

        books_info.append({
            "book_id": book['book_id'],
            "title": book['title'],
            "author": book['author'],
            "borrow_date": book['borrow_date'].strftime("%Y-%m-%d"),
            "due_date": book['due_date'].strftime("%Y-%m-%d"),
            "days_overdue": days_overdue,
            "late_fee": round(fee_amount, 2)
        })

    #Return the dictonary 
    return {
        "patron_id": patron_id,
        "currently_borrowed": books_info,
        "total_late_fees": round(total_late_fees, 2),
        "amount_of_books_borrowed": len(borrowed_books)
    }
