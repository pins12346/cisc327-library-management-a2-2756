### Brian Minkovich, Student ID: 20282756

| Function Name | Implementation Status | What Is Missing |
| ------------- | --------------------- | --------------- |
| add_book_to_catalog (library_service.py) | Completed | N/A |
| catalog (catalog_routes.py) | Completed | N/A |
| borrow_book_by_patron (library_service.py) | Partial | This feature is implemented, however in the code, it checks if borrow books is > 5, which will allow users to borrow 6. It should be >= 5, so that the program gives the error message when it is 5 books and not 6. |
| return_book_by_patron (library_service.py)| Partial | <br> - Verification that the book was borrowed by the patron is missing.  <br> - The updating of the records is missing.  <br>- The calculating and displaying of any late fees is missing. <br>- It is also missing any input validation for the input of the function.  |
| calculate_late_fee_for_book (library_service.py)| Partial | <br>-  It is missing all of the calculation logic. <br>- The return statement is commented out so it currently does not do anything as it is a part of the doc string and the function currently does not return anything. <br>- It is also missing input validation. <br>- Also, there is no API route as described in the requirements specification file. |
| search_books_in_catalog (library_service.py) | Partial | <br>- This function is currently missing a way to read the input and get the 'q' and "type" variables from the passed in list. <br>- As well, it is missing the logic for the partial matching for title and author as well as the exact matching for the ISBN.<br>-  Currently this function also returns an empty list and is missing a proper return statement.<br>-  It is also missing input validation. |
| get_patron_status_report (library_service.py) | Partial |<br>-  Currently this function is missing the logic to get the status report for a particular patron, and does not gather any of the four requested things to be displayed. <br>- It also currently returns an empty dictonary and has no input validation on the patron string.  |


## Summary Of The Tests: 
For each function in Library Service.py, several different input validation tests have been created. Testing things like if the book title is more than 200 characters, if the author is more than 100 characters. Also testing data types like if input types are incorrect (for example if the function asks for a number and instead gets an a string), or if None is passed in the function. These tests are critical to the program because when deploying an application, users will try and input a wide variety of things and thus it is important to test all input cases. As well, features are tested like ensuring that the correct borrow limits are in place and that the program is working as intended



## Function Name: add_book_to_catalog (library_service.py) Status: Completed 
Summary: <br><br>
test_add_book_valid_input -> Passed, currently the test book is in the database, so in future this test will fail.

test_add_book_invalid_isbn_too_short -> Passed, the function will return false and the correct message in the case that the ISBN is too short. 

test_add_book_title_too_long -> Passed, the function will return the proper message.

test_add_book_author_too_long -> Passed, the function will return the proper message.

test_add_book_negative_copies -> Passed, the function will return the proper message. 

## Function Name:  borrow_book_by_patron (library_service.py) Status: Completed 
Summary: <br> <br>

test_borrow_book_by_patron_valid_input -> Passed, book used was the test book added (ID: 4), and correct message is output.

test_borrow_book_by_patron_ID_letters -> Passed, the function returned false and the correct message in the case that a string was entered for patron ID.

test_borrow_book_by_patron_ID_too_long -> Passed, The function returned false and the correct message in the case that patron ID was too long.

test_borrow_book_by_patron_ID_too_short -> Passed, the function returned false and the correct message in the case that the patron ID was too short.  

test_borrow_book_by_patron_6_books -> Failed, this test should pass as users shoudlnt be able to take out 6 books but because of the bug, they are able to.



## Function Name: return_book_by_patron (library_service.py) Status: Partial 
Summary: <br> <br>

test_return_book_by_patron_valid_input -> Failed, This test assumes that the return_book_by_patron has been implemented already which it has not. The function returns false and "Book return functionality is not yet implemented".

test_return_book_by_patron_null_book_id -> Failed, This test assumes that the return_book_by_patron has been implemented already which it has not. The function returns false and "Book return functionality is not yet implemented". The test assumes that there is input validatiion and is aiming to test if nothing was entered in Book ID that the function could handle it.

test_return_book_by_patron_string_as_book_id ->Failed, This test assumes that the return_book_by_patron has been implemented already which it has not. The function returns false and "Book return functionality is not yet implemented". The test assumes that there is some input validation for book ID and is aiming to test that.

test_return_book_by_patron_id_as_string -> Failed, This test assumes that the return_book_by_patron has been implemented already which it has not. The function returns false and "Book return functionality is not yet implemented". The test assumes that there is some input validation for patron ID and aims to test that.

test_return_book_dne -> Failed, This test assumes that the return_book_by_patron has been implemented already which it has not. The function returns false and "Book return functionality is not yet implemented". The test assumes that there is some way for the function to tell if a book does not exist.

test_return_book_twice -> Failed, This test assumes that the return_book_by_patron has been implemented already which it has not. The function returns false and "Book return functionality is not yet implemented". The test assumes that there is some way for the function to tell if a book  cannot be returned.

## Function Name: calculate_late_fee_for_book (library_service.py) Status: Partial 
Summary: <br> <br>

test_calculate_late_fee_for_book_valid_input -> Failed, this test assumes that the function has been implemented already which it has not been. It aims to test and ensure that the function is working as intended. Currently the function does not return anything.

test_calculate_late_fee_for_book_null_patron_id -> Failed, this test assumes that the function has been implemented already which it has not been. It aims to test what happens when nothing is passed in for Patron ID. Currently the function does not return anything.

test_calculate_late_fee_for_book_ID_book_title -> Failed, this test assumes that the function has been implemented already which it has not been. It aims to test what happens when a book title is passed in for Patron ID. Currently the function does not return anything.

test_calculate_late_fee_for_book_no_input -> Failed, this test assumes that the function has been implemented already which it has not been. Nothing is passed into the function (both book ID and patron ID). Currently the function does not return anything.

test_calculate_fee_overdue_cap -> Failed, this test assumes that the function has been implemented already which it has not been. It aims to test the cap on the fee for late books. Currently the function does not return anything.

## Function Name: search_books_in_catalog (library_service.py) Status: Partial 
Summary: <br> <br>

test_search_books_in_catalog_valid_input -> Failed, this test assumes that the function has been implemented already which it does not. The assert statements test to see if the length of the list of dictonaries is greater than one. Since all the function does right now is return an empty list, this test fails. 

test_search_books_in_catalog_invalid_type -> Passed, although this function is not implemented, it is assumed that once it is upon failing the function will still return an empty list, hence why the only checks are for it returning an empty list. The goal of this test is to check how the function handles a miss-match in search type and what is searched. 

test_search_books_in_catalog_invalid_title -> Passed, although this function is not implemented, it is assumed that once it is upon failing the function will still return an empty list, hence why the only checks are for it returning an empty list. The goal of this test is to check how the function handles too long if a title searched. 

test_search_books_in_catalog_invalid_ISBN -> Passed, although this function is not implemented, it is assumed that once it is upon failing the function will still return an empty list, hence why the only checks are for it returning an empty list. The goal of this test is to see how the function handles an invalid ISBN being searched.

## Function Name: get_patron_status_report (library_service.py) Status: Partial 
Summary: <br> <br>

test_get_patron_status_report_valid_input -> Failed, this test assumes that the function has been implemented already which it has not. Currently all the fucntion returns is an empty dictonary. The test assumes that the dictonary would have the specified keys in the requirments that the function hs to fulfil. 

test_get_patron_status_report_null_id -> Passed, although this function is not implemented, it is assumed that once it is, upon failing the function will still return an empty dictonary, hence why the only checks are for it returning an empty dictonary. The goal of this test is to see how the function handles an null patron ID.

test_get_patron_status_report_Book_Title_as_Patron_ID -> Passed, although this function is not implemented, it is assumed that once it is, upon failing the function will still return an empty dictonary, hence why the only checks are for it returning an empty dictonary. The goal of this test is to see how the function handles an string patron ID.

test_get_patron_status_report_int_as_patron_id ->
Passed, although this function is not implemented, it is assumed that once it is, upon failing the function will still return an empty dictonary, hence why the only checks are for it returning an empty dictonary. The goal of this test is to see how the function handles a too long patron ID.

test_get_patron_status_report_patron_id_nothing_taken_out -> Passed,  although this function is not implemented, it is assumed that once it is, upon failing the function will still return an empty dictonary, hence why the only checks are for it returning an empty dictonary. The goal of this test is to see how the function handles a patron with nothing taken out.
