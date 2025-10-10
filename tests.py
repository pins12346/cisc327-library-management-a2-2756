import pytest
from library_service import (
    add_book_to_catalog
)
from library_service import(
    borrow_book_by_patron
)
from library_service import(
    return_book_by_patron
)
from library_service import(
    calculate_late_fee_for_book
)

from library_service import(
    search_books_in_catalog
)

from library_service import(
    get_patron_status_report
)

from database import(
    get_book_by_isbn
)

'''
These tests assume that the database has just been created and the sample data is the only thing in the database

NOTE: The github CI pipeline was giving me issues with the test script being in the test folder so I created a new 
file in the main directory called tests.py and it contains the same content as test.py in the test folder, I just run 
tests.py in the CI workflow. I hope this is okay, I tried trouble shooting for a while and couldnt figure it out
'''


#book_to_catalog







def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert f'book Test Book has been successfully added to the catalog.' in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "ISBN must be exactly 13 digits." in message

def  test_add_book_title_too_long():
    """Test adding a book with too long of a title."""
    success,message = add_book_to_catalog("sdfmasmflaksdfk;ldsmfkl;asdmfklasdmfwklwwwmsvkldmsvklanlfkajflkjasdfklasdnalsdnvjlasdnvajdsnvaljdvnajdndsdfmasmflaksdfk;ldsmfkl;asdmfklasdmfklmsvkldmsvklanlfkajflkjasdfklasdnalsdnvjlasdnvajdsnvaljdvnajdnd", "Test Author", "1234567897777", 5)
    
    assert success == False
    assert "Title must be less than 200 characters." in message
    
def test_add_book_author_too_long():
    """Test adding an author with 100 characters"""
    success, message = add_book_to_catalog("Test Book", "sdfmasmflaksdfk;ldsmfkl;asdwmfklwwwasdmfklmsvkldmsvklanlfkajflkjasdfklasdnalsdnvjlasdnvajdsnvaljdvnajdnd", "1234567866666", 5)
    
    assert success == False
    assert "Author must be less than 100 characters." in message

def test_add_book_not_valid_copies():
    '''Testing negative book copies '''
    
    success, message = add_book_to_catalog("Test Book", "Author", "1234567895768", -2)
    
    assert success == False
    assert "Total copies must be a positive integer." in message
    
    
    
    
    
#borrow_book_by_patron
    
    
    
    
    
    
    
def test_borrow_book_by_patron_valid_input():
    """Test Proper Input"""
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890179", 5)
    #get the book by the ispn
    book = get_book_by_isbn("1234567890179")
    success, message = borrow_book_by_patron("123456", book['id'])
    print(message)
    assert success == True
    assert "successfully borrowed" in message.lower()
    
def test_borrow_book_by_patron_ID_letters():
    """Test Validation for letters On ID"""
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890127", 5)
    #get the book by the ispn
    book = get_book_by_isbn("1234567890127")
    success, message = borrow_book_by_patron("Chains" , book["id"])
    
    assert success == False
    assert "Invalid patron ID. Must be exactly 6 digits." in message

def test_borrow_book_by_patron_ID_too_long():
    """Test ID too long"""
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890155", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567890155")
    success, message = borrow_book_by_patron("1234567" , book["id"])
    
    assert success == False
    assert "Invalid patron ID. Must be exactly 6 digits." in message

def test_borrow_book_by_patron_ID_too_short():
    """Test ID too Short"""
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890144", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567890144")
    success, message = borrow_book_by_patron("123" , book['id'])
    
    assert success == False
    assert "Invalid patron ID. Must be exactly 6 digits." in message

def test_borrow_book_by_patron_6_books():
    ''' Test 6 Books Being Borrowed'''
    #add the book to the database
    add_book_to_catalog("Test Book 3", "Test Author", "1234567890133", 6)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567890133")
    borrow_book_by_patron("123459" , book['id'])
    borrow_book_by_patron("123459" , book['id'])
    borrow_book_by_patron("123459" , book['id'])
    borrow_book_by_patron("123459" , book['id'])
    borrow_book_by_patron("123459" , book['id'])
    success, message= borrow_book_by_patron("123459" , book['id'])
    
    assert success == False
    assert "You have reached the maximum borrowing limit of 5 books." in message
    
def test_borrow_unavailable_book():
    
    #add the book to the database
    add_book_to_catalog("Test Book 3", "Test Author", "1234567890132", 0)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567890132")
    success, message = borrow_book_by_patron("123454" , book['id'])
    assert success == False
    assert "This book is currently not available." in message
    
    
    
    
    
    
    
    
    
#return_book_by_patron








def test_return_book_by_patron_valid_input():
    """Test Proper Input"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567898546", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567898546")
    #borrow the book
    borrow_book_by_patron("122456", book['id'])
    
    success, message = return_book_by_patron("122456" , book['id'])
    
    assert success == True
    assert f'Successfully returned "{book["title"]}".' in message.lower()
    
def test_return_book_by_patron_null_book_id():
    """Test ID Null"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567898543", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567898543")
    #borrow the book
    borrow_book_by_patron("124456", book['id'])
    
    success, message = return_book_by_patron("124456" , None)
    
    assert success == False
    assert "Book not found." in message
    
def test_return_book_by_patron_string_as_book_id():
    """Test ID String"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567898541", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567898541")
    #borrow the book
    borrow_book_by_patron("123556", book['id'])
    
    success, message = return_book_by_patron("123556" , "Test Title")
    
    assert success == False
    assert "Book not found." in message
    
def test_return_book_by_patron_id_as_string():
    """Test ID as string"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567898540", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567898540")
    #borrow the book
    borrow_book_by_patron("123956", book['id'])
    
    success, message = return_book_by_patron("Test Title", book['id'])
    
    assert success == False
    assert "Book not found." in message
    
def test_return_book_dne():
    '''Testing returning a book that was not taken out by that patron'''
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567898530", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567898530")
    #borrow the book
    borrow_book_by_patron("123356", book['id'])
    
    success, message = return_book_by_patron("123356", book['id'])
    
    assert success == False
    assert f'You have not borrowed "{book["title"]}".' in message

def test_return_book_twice():
    ''' Testing returning the same book twice'''
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567598530", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567598530")
    #borrow the book
    borrow_book_by_patron("123336", book['id'])
    
    success, message = return_book_by_patron("123336", book['id'])
    
    assert success == True
    
    success, message = return_book_by_patron("123336", book['id'])
    assert success == False
    assert f'You have not borrowed "{book["title"]}".' in message
    
    
    
    
    
    
#calculate_late_fee_for_book







def test_calculate_late_fee_for_book_valid_input():
    """Test Proper Input"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890111", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567890111")
    #borrow the book
    borrow_book_by_patron("123256", book['id'])
    
    result = calculate_late_fee_for_book("123256", book['id'])

    assert isinstance(result, dict)
    assert "fee_amount" in result 
    assert "days_overdue" in result
    assert "status" in result 
    assert result["status"] == "Success"


def test_calculate_late_fee_for_book_null_patron_id():
    """Test Null ID"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890112", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567890112")
    #borrow the book
    borrow_book_by_patron("123459", book['id'])
   
    
    
    result = calculate_late_fee_for_book(None, book['id'])
    
    assert isinstance(result, dict) 
    assert "fee_amount" in list(result.keys()) 
    assert "days_overdue" in list(result.keys())
    assert "status" in list(result.keys())
    assert "Failed" in result["status"]
    

def test_calculate_late_fee_for_book_ID_book_title():
    """Test Patron ID Book Title"""
   
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890158", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234567890158")
    #borrow the book
    borrow_book_by_patron("123496", book['id'])
    
    
    result = calculate_late_fee_for_book("Test Book", book['id'])
    
    assert isinstance(result, dict) 
    assert "fee_amount" in list(result.keys()) 
    assert "days_overdue" in list(result.keys())
    assert "status" in list(result.keys())
    assert "Book not found." in result["status"]
    

def test_calculate_late_fee_for_book_no_input():
    """Test No Given Input"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567890119", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("123456789018")
    #borrow the book
    borrow_book_by_patron("123416", book['id'])
    
    
    result = calculate_late_fee_for_book(None, None)
    
    assert isinstance(result, dict) 
    assert "fee_amount" in list(result.keys()) 
    assert "days_overdue" in list(result.keys())
    assert "status" in list(result.keys())
    assert "Book not Found." in result["status"]

import datetime
from database import insert_borrow_record
    
def test_calculate_fee_overdue_cap():
    ''' Test the limit of 15 dollars on the late fee'''
    add_book_to_catalog("Test Book", "Test Author", "1234560890119", 5)
    book = get_book_by_isbn('1234560890119')
    insert_borrow_record("000012", book['id'], datetime.datetime.now() - datetime.timedelta(days=60), datetime.datetime.now() - datetime.timedelta(days=46))
    result = calculate_late_fee_for_book("000012", book['id'])
    
    assert isinstance(result, dict) 
    assert "fee_amount" in list(result.keys()) 
    assert "days_overdue" in list(result.keys())
    assert "status" in list(result.keys())
    assert result["fee_amount"] == 15.00
    
    


#search_books_in_catalog







    
def test_search_books_in_catalog_valid_input():
    """Test Proper Input"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567777123", 5)

    result = search_books_in_catalog("Test Book", "title")
    
    assert isinstance(result, list)
    assert len(result) >= 1
    assert "Test Book" in result
    
def test_search_books_in_catalog_invalid_type():
    """Test Invalid Type Of Search"""
    
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567777122", 5)

    
    result = search_books_in_catalog("Test Title", "Patron ID")
    
    assert isinstance(result, list)
    assert result == []
    
def test_search_books_in_catalog_invalid_title():
    """Test Too Long Title"""
    
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567777127", 5)

    
    result = search_books_in_catalog("dlfhadhvakvbdsvbsdahvgbdkslhvsdakljvhdlsjkavbsdalkjvnsdakljvndsakjnvdaslkjnvadskljfhkjdlshfkjlasdbcvkjladsncvkaljsdbvlkjadhvadlkjsbvadlskjvbakljvbadklsjvbakljvbdakljvbadljkvbadsljkvablkjvbdasjklcajklchaskjlc", "Title")
    
    assert isinstance(result, list)
    assert result == []
    
def test_search_books_in_catalog_invalid_ISBN():
    """Test Invalid ISBN"""
    
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567777129", 5)

    result = search_books_in_catalog("123456789012345", "ISBN")
    
    assert isinstance(result, list)
    assert result == []
    
    
    
    
    
    
#get_patron_status_report







def test_get_patron_status_report_valid_input():
    """Test Valid Input"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234555590123", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234555590123")
    #borrow the book
    borrow_book_by_patron("123056", book['id'])
    
    result = get_patron_status_report("123056")

    assert isinstance(result, dict)
    #Assuming this is what output could look like based on the requirements
    assert "currently_borrowed" in list(result.keys())
    assert book['title'] in result["currently_borrowed"]["title"]
    assert "late_fee" in list(result.keys())
    assert "amount_of_books_borrowed" in list(result.keys())
    assert "patron_id" in list(result.keys())
    assert result["patron_id"] == "123056"
    


def test_get_patron_status_report_null_id():
    """Test Null Patron ID"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234555590121", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234555590121")
    #borrow the book
    borrow_book_by_patron("123451", book['id'])
    
    result = get_patron_status_report(None)
   
    assert isinstance(result, dict)
    assert result == {"error": "Invalid patron ID."}
    
    
def test_get_patron_status_report_Book_Title_as_Patron_ID():
    """Test Book Title as Patron ID"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234555590128", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234555590128")
    #borrow the book
    borrow_book_by_patron("123450", book['id'])
    
    result = get_patron_status_report("Test Title")
    assert isinstance(result, dict)
    assert result == {"error": "Invalid patron ID."}
    
    
def test_get_patron_status_report_patron_id_too_long():
    """Test too long Patron ID"""
    
    #add the book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234555590127", 5)
    #get the book by the ispn 
    book = get_book_by_isbn("1234555590127")
    #borrow the book
    borrow_book_by_patron("023456", book['id'])
    
    result = get_patron_status_report("0234586")
    assert isinstance(result, dict)
    assert result == {"error": "Invalid patron ID."}
    
    
def test_get_patron_status_report_patron_id_nothing_taken_out():
    """Test when patron hasn't taken anything out"""
    
    
    result = get_patron_status_report("024586")
    assert "currently_borrowed" in list(result.keys())
    assert result["currently_borrowed"] == []
    assert "late_fee" in list(result.keys())
    assert "amount_of_books_borrowed" in list(result.keys())
    assert "patron_id" in list(result.keys())
    
    
    

