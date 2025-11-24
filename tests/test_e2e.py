import subprocess
import time
import requests
from playwright.sync_api import sync_playwright

#Start Flask app for testing

def start_flask_app():
    server = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    #Waiting until server is ready
    for _ in range(25):
        try:
            requests.get("http://localhost:5000")
            return server
        except:
            time.sleep(0.3)

    raise RuntimeError("Flask server did not start")


#Creating browser once per fle 

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=True)


#Add book and verify in catalog

def test_add_book_and_catalog():
    server = start_flask_app()

    page = browser.new_page()
    page.goto("http://localhost:5000/add_book")

    page.fill("input[name='title']", "E2E Test Book")
    page.fill("input[name='author']", "Author Tester")
    page.fill("input[name='isbn']", "9876543210123")
    page.fill("input[name='total_copies']", "4")

    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")

    page.goto("http://localhost:5000/catalog")
    page.wait_for_selector("text=E2E Test Book", timeout=5000)

    server.terminate()


#Borrow a book 

def test_borrow_book():
    server = start_flask_app()

    page = browser.new_page()
    page.goto("http://localhost:5000/catalog")

    borrow_form = page.query_selector("form[action='/borrow']")
    if borrow_form is None:
        server.terminate()
        raise RuntimeError("No borrow forms found in catalog")

    #Fill in the patron ID
    patron_input = borrow_form.query_selector("input[name='patron_id']")
    patron_input.fill("123456") 

    borrow_button = borrow_form.query_selector("button[type='submit']")
    borrow_button.click()

    page.wait_for_load_state("networkidle")

    #After it reloads, we query the page again to verify book ID exists
    new_book_input = page.query_selector("input[name='book_id']")
    if new_book_input is None:
        print("Borrow successful - book input not found on catalog page (expected if unavailable)")
    else:
        book_id = new_book_input.get_attribute("value")
        print(f"Book {book_id} still in catalog")

    server.terminate()


#Close Browser after tests

def teardown_module():
    browser.close()
    pw.stop()
