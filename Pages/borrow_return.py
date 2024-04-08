import streamlit as st
import requests
import datetime
from Pages.HashingURL import hash_book, get_book_path, get_user_path, hash_user


# Firebase Realtime Database URL


def fetch_book_data(book_id):
    """Fetches data for a specific book by ID."""
    FIREBASE_URL =  get_book_path(hash_book(int(book_id)))
    response = requests.get(f"{FIREBASE_URL}/{book_id}.json")
    if response.ok:
        return response.json()
    return None


def update_book_availability(book_id, option=None):
    """Updates the book's availableNums in the database."""
    book_data = fetch_book_data(book_id)
    print(book_data)
    response = None  # Initialize response to None
    if book_data:
        FIREBASE_URL = get_book_path(hash_book(int(book_id)))
        num_change = 1 if option != 'borrow' else -1
        new_count = book_data.get('availableNums', 0) + num_change
        response = requests.patch(f"{FIREBASE_URL}/{book_id}.json", json={"availableNums": new_count})

    # Check if response has been set and is okay before returning
    print(response)
    if response and response.ok:
        return True
    else:
        # Handle the case where the response is not okay or the book_data does not exist
        return False

def fetch_user_loans(user_id):
    USER_URL = get_user_path(hash_user(int(user_id)))
    user_loans_url = f"{USER_URL}/{user_id}/books.json"
    response = requests.get(user_loans_url)
    return response.json() if response.json() else []

def update_user_loans(user_id, book_id, action, days = None):
    user_loans_url = get_user_path(hash_user(int(user_id)))
    loans = fetch_user_loans(user_id)

    if action == "borrow":
        start_date = datetime.datetime.now()
        due_date = (start_date + datetime.timedelta(days = days)).strftime('%Y-%m-%d')
        loans.append({"book_id": book_id, "start_date": start_date.strftime('%Y-%m-%d'), "due_date": due_date, "status": "borrowing"})
        resp = requests.put(f'{user_loans_url}/{user_id}/books.json', json = loans)
        return resp.ok
    else: 
        for loan in loans:
            if loan["book_id"] == book_id and loan["status"] == "borrowing":
                due = datetime.datetime.strptime(loan['due_date'], "%Y-%m-%d")
                if due >= datetime.datetime.now():
                    loan["status"] = 'returned'
                else: 
                    loan["status"] = 'overdue returned'
                break  # Assuming only one active loan per book
        resp = requests.put(f'{user_loans_url}/{user_id}/books.json', json = loans)
        return loan["status"], resp.ok


def borrow_book_page():
    st.title("Borrow")
    book_id = st.text_input("Enter the ID of your book to Borrow")
    days_to_borrow = st.number_input("Days to Borrow", min_value=1, value=14)
    
    if st.button("Confirm"):
        book_data = fetch_book_data(book_id)
        if book_data and book_data.get('availableNums', 0) > 0:
            update = update_book_availability(book_id, option = 'borrow')
            if update:
                user_id = st.session_state['userid'] # Example: retrieve user_id from session state
                resp = update_user_loans(user_id, book_id, 'borrow', days = days_to_borrow)
                if resp:
                    st.success(f"Successfully borrowed {book_id}: < {book_data['title']} >.")
                else: 
                    st.error('Cannot update user loans.')
            else:
                st.error('Cannot update book stock.')
        else:
            st.error("Sorry, the book is out of stock.")

def return_book_page():
    st.title("Return")
    book_id = st.text_input("Enter the Book ID to Return")
    
    if st.button("Confirm Return"):
        userid = st.session_state['userid']
        user_loans = fetch_user_loans(userid)

        # No Borrowed book.
        if not user_loans:
            st.warning('No record. Please check again.')
            return 
        for loan in user_loans:
            if loan['book_id'] == book_id and loan['status'] == 'borrowing':
                # If there is matched records and if overdue.
                if update_book_availability(book_id, option = 'return'):
                    status, resp = update_user_loans(userid, book_id, "return")
                    if resp:
                        book_data = fetch_book_data(book_id)
                        if status == 'returned':
                            st.success(f"Successfully returned {book_id}: {book_data['title']}.")
                        else:
                            st.error(f"Overdue <{book_id}: {book_data['title']}>.")
                            st.success(f"Successfully returned.")
                    else:
                        st.error('Cannot update user returns.')
                else:
                    st.error(f'We do not have this book <isbn: {book_id}>.')
                return 
        st.warning('No record. Please check again.')
        return
            
            
def borrow_return_page():
    st.title("Borrow/Return Books")
    # Initialize action in session_state
    if 'action' not in st.session_state:
        st.session_state['action'] = None

    col1, col2 = st.columns(2)  # Simplified to two columns for borrow and return

    with col1:
        if st.button("Borrow"):
            st.session_state['action'] = 'borrow'
            #st.experimental_rerun()
    with col2:
        if st.button("Return"):
            st.session_state['action'] = 'return'
            #st.experimental_rerun()

    # Conditional rendering based on the chosen action
    if st.session_state['action'] == 'borrow':
        borrow_book_page()
    elif st.session_state['action'] == 'return':
        return_book_page()

