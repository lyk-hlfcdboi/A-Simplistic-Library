import streamlit as st
import requests
import pandas as pd
from Pages import user_auth
from Pages import HashingURL
import datetime

# Firebase Realtime Database URL

def fetch_user_loans(user_id):
    """Fetches loan information for a specific user."""
    FIREBASE_URL = HashingURL.get_user_path(HashingURL.hash_user(int(user_id)))

    response = requests.get(f"{FIREBASE_URL}/{user_id}/books.json")
    if response.ok:
        if len(response.json()) == 1:
            return []
    res = response.json()
    del res['NoBorrowedBook']
    return res

def format_and_sort_loans(loans):
    """Formats loans data and sorts it by status, borrow on, and due to."""
    data = []
    for bid, rec in loans.items():
        rec.update({'book_id': bid})
        data.append(rec)
    del loans
    print(data)
    df = pd.DataFrame(data)
    df = df[["book_id", "start_date", "due_date"]]
    df.columns = ['Book ID', 'Start Date', 'Return Date']
    today = datetime.datetime.now().date()

    df['Status'] = pd.to_datetime(df['Return Date']).apply(lambda due: 'Borrowing' if due.date() >= today else 'Overdue')
    df.sort_values(by = ['Start Date', 'Return Date'], ascending = [False, False], inplace=True)
    return df

def account_management_page():
    if 'login_status' in st.session_state and st.session_state['login_status'] == 'LS':
        user_id = st.session_state['userid']
        # Current time
        st.write(f'Refreshed at: {datetime.datetime.now().replace(microsecond = 0)}')

        # Fetch and process user loan information
        loans = fetch_user_loans(user_id)
        print(loans)
        if loans:
            df = format_and_sort_loans(loans)
            df_html = df.head(15).to_html(index=False)
            st.write('\n\n\n')

            st.title('Borrowing')
            st.write(df_html, unsafe_allow_html = True)
            st.write(f"\n\nBooks borrowing: {len(loans)}")
        else:
            st.write("No borrow/return record found.")

        if st.button('Log Out'):
            # Clear user-specific session state variables
            st.session_state.clear()
            st.success("You have been logged out.")
    else:
        st.warning("Please login first.")
        user_auth.render_login_signup()

# Example call to this function; you would typically do this from your main app script
if __name__ == "__main__":
    account_management_page()
