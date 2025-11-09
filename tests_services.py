from unittest.mock import Mock, patch
from library_service import pay_late_fees, refund_late_fee_payment

#Stubs for DB/business functions 
def stub_db_functions():
    patch("library_service.calculate_late_fee_for_book", return_value={"fee_amount": 10.0, "days_overdue": 5, "status": "Success"}).start()
    patch("library_service.get_book_by_id", return_value={"id": 1, "title": "Test Book"}).start()

def stub_zero_fee():
    patch("library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0.0, "days_overdue": 0, "status": "Success"}).start()

#Mocks for Payment Gateway 
def mock_gateway():
    return Mock(spec=["process_payment", "refund_payment"])

#Tests for pay_late_fees 

#Test Successful Payment 
def test_successful_payment():
    stub_db_functions()
    mock = mock_gateway()
    mock.process_payment.return_value = (True, "txn_123", "Payment OK")

    success, message, txn = pay_late_fees("123456", 1, mock)

    mock.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=10.0,
        description="Late fees for 'Test Book'"
    )

    assert success is True
    assert "Payment successful" in message or "Payment OK" in message or txn == "txn_123"

#Payment Declined Test  
def test_payment_declined():
    stub_db_functions()
    mock = mock_gateway()
    mock.process_payment.return_value = (False, "", "Declined: insufficient funds")

    success, message, txn = pay_late_fees("123456", 1, mock)

    mock.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=10.0,
        description="Late fees for 'Test Book'"
    )

    assert success is False
    assert txn is None
    assert "Payment failed" in message and "Declined" in message

#Invalid Patron ID Test 
def test_invalid_patron_id():
    mock = mock_gateway()
    success, message, txn = pay_late_fees("INVALID", 1, mock)

    mock.process_payment.assert_not_called()
    assert success is False
    assert txn is None
    assert "Invalid patron ID" in message

#Test Zero Late Fee 
def test_zero_late_fee():
    stub_zero_fee()
    mock = mock_gateway()
    success, message, txn = pay_late_fees("123456", 1, mock)

    mock.process_payment.assert_not_called()
    assert success is False
    assert txn is None
    assert "No late fees to pay" in message

#Test Network Error 
def test_network_error():
    stub_db_functions()
    mock = mock_gateway()
    mock.process_payment.side_effect = ConnectionError("Network failure")

    success, message, txn = pay_late_fees("123456", 1, mock)

    mock.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=10.0,
        description="Late fees for 'Test Book'"
    )

    assert success is False
    assert txn is None
    assert "Payment processing error" in message and "Network failure" in message

#Tests for Late Payment Refunds 
def test_successful_refund():
    mock = mock_gateway()
    mock.refund_payment.return_value = (True, "Refund processed. Refund ID: rf_1")

    success, message = refund_late_fee_payment("txn_abc", 5.0, mock)

    mock.refund_payment.assert_called_once_with("txn_abc", 5.0)

    assert success is True
    assert "Refund" in message or "processed" in message

#Testing Invalid Transaction ID 
def test_invalid_transaction_id():
    mock = mock_gateway()
    success, message = refund_late_fee_payment("", 5.0, mock)

    mock.refund_payment.assert_not_called()
    assert success is False
    assert "Invalid transaction ID" in message

#Testing invalid refund amounts  
def test_invalid_refund_amounts():
    mock = mock_gateway()
    for amount in [-5, 0, 16]:
        success, message = refund_late_fee_payment("txn_abc", amount, mock)
        mock.refund_payment.assert_not_called()
        assert success is False
        assert ("Invalid refund amount" in message) or ("exceeds maximum late fee" in message) or ("Refund amount must be greater than 0" in message)
