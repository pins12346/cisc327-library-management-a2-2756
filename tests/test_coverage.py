from unittest.mock import patch, Mock
from services import library_service
from services.payment_service import PaymentGateway

# Stubs for database and business logic functions

def stub_existing_book():
    patch("services.library_service.get_book_by_isbn", return_value={"isbn": "1234567890123"}).start()

def stub_non_existing_book():
    patch("services.library_service.get_book_by_isbn", return_value=None).start()

def stub_insert_book(success=True):
    patch("services.library_service.insert_book", return_value=success).start()

def stub_get_book(book_data):
    patch("services.library_service.get_book_by_id", return_value=book_data).start()

def stub_borrow_data(borrowed_books=None, count=0):
    patch("services.library_service.get_patron_borrowed_books", return_value=borrowed_books or []).start()
    patch("services.library_service.get_patron_borrow_count", return_value=count).start()

def stub_update(success=True):
    patch("services.library_service.update_book_availability", return_value=success).start()
    patch("services.library_service.update_borrow_record_return_date", return_value=success).start()

def stub_late_fee(fee=0.0):
    patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": fee}).start()


# Tessts for add_book_to_catalog



def test_add_book_duplicate_isbn():
    stub_existing_book()
    success, msg = library_service.add_book_to_catalog("Book", "Author", "1234567890123", 5)
    assert success is False 
    assert "already exists" in msg

def test_add_book_db_error():
    stub_non_existing_book()
    stub_insert_book(False)
    success, msg = library_service.add_book_to_catalog("Book", "Author", "1234567890123", 5)
    assert success is False 
    assert "Database error" in msg

def test_add_book_success():
    stub_non_existing_book()
    stub_insert_book(True)
    success, msg = library_service.add_book_to_catalog("Book", "Author", "1234567890123", 5)
    assert success is True 
    assert "successfully added" in msg


# Tests for borrow_book_by_patron

def test_borrow_insert_error():
    stub_get_book({"id": 1, "title": "Book", "available_copies": 1})
    stub_borrow_data(count=1)
    patch("services.library_service.insert_borrow_record", return_value=False).start()
    success, msg = library_service.borrow_book_by_patron("123456", 1)
    assert success is False 
    assert "creating borrow record" in msg

def test_borrow_update_error():
    stub_get_book({"id": 1, "title": "Book", "available_copies": 1})
    stub_borrow_data(count=1)
    patch("services.library_service.insert_borrow_record", return_value=True).start()
    patch("services.library_service.update_book_availability", return_value=False).start()
    success, msg = library_service.borrow_book_by_patron("123456", 1)
    assert success is False 
    assert "updating book availability" in msg

# Tests for return_book_by_patron


def test_return_db_error():
    stub_get_book({"id": 1, "title": "Book"})
    borrowed_books = [{"book_id": 1, "title": "Book"}]
    patch("services.library_service.get_patron_borrowed_books", return_value=borrowed_books).start()
    stub_late_fee(0.0)
    patch("services.library_service.update_borrow_record_return_date", return_value=False).start()
    patch("services.library_service.update_book_availability", return_value=True).start()
    success, msg = library_service.return_book_by_patron("123456", 1)
    assert success is False 
    assert "processing return" in msg

def test_return_success_with_fee():
    stub_get_book({"id": 1, "title": "Book"})
    borrowed_books = [{"book_id": 1, "title": "Book"}]
    patch("services.library_service.get_patron_borrowed_books", return_value=borrowed_books).start()
    stub_late_fee(3.5)
    stub_update(True)
    success, msg = library_service.return_book_by_patron("123456", 1)
    assert success is True 
    assert "Late fee" in msg



# More tests for payment_service 



# Process payment test

def test_process_payment_invalid_amount_zero():
    gateway = PaymentGateway()
    success, txn, msg = gateway.process_payment("123456", 0)
    assert success is False
    assert "Invalid amount" in msg

def test_process_payment_invalid_amount_negative():
    gateway = PaymentGateway()
    success, txn, msg = gateway.process_payment("123456", -5.0)
    assert success is False
    assert "Invalid amount" in msg

def test_process_payment_amount_exceeds_limit():
    gateway = PaymentGateway()
    success, txn, msg = gateway.process_payment("123456", 1500.0)
    assert success is False
    assert "exceeds limit" in msg

def test_process_payment_invalid_patron_id_length():
    gateway = PaymentGateway()
    success, txn, msg = gateway.process_payment("123", 10.0)
    assert success is False
    assert "Invalid patron ID" in msg

# Refund payment tests 

def test_refund_payment_invalid_transaction_id():
    gateway = PaymentGateway()
    success, msg = gateway.refund_payment("bad_txn", 10.0)
    assert success is False
    assert "Invalid transaction ID" in msg

def test_refund_payment_empty_transaction_id():
    gateway = PaymentGateway()
    success, msg = gateway.refund_payment("", 10.0)
    assert success is False
    assert "Invalid transaction ID" in msg

def test_refund_payment_invalid_refund_amount():
    gateway = PaymentGateway()
    success, msg = gateway.refund_payment("txn_123456_1234567890", 0)
    assert success is False
    assert "Invalid refund amount" in msg
