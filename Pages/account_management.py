import streamlit as st
import requests
import pandas as pd
from Pages import user_auth
from Pages import HashingURL


# Firebase Realtime Database URL

def fetch_user_loans(user_id):
    """Fetches loan information for a specific user."""
    FIREBASE_URL = HashingURL.get_user_path(HashingURL.hash_user(int(user_id)))

    response = requests.get(f"{FIREBASE_URL}/{user_id}/books.json")
    if response.ok:
        if isinstance(response.json(), dict):
            return []
    return response.json()

def format_and_sort_loans(loans):
    """Formats loans data and sorts it by status, borrow on, and due to."""
    df = pd.DataFrame(loans)
    df = df[["book_id","start_date","due_date","status"]]
    df.columns = ['Book ID', 'Start Date', 'Return Date', 'Status']
    df.sort_values(by = ['Start Date', 'Return Date', 'Status'], inplace=True)
    return df

def account_management_page():
    if 'login_status' in st.session_state and st.session_state['login_status'] == 'LS':
        user_id = st.session_state['userid']
        
        # Fetch and process user loan information
        loans = fetch_user_loans(user_id)
        if loans:
            df = format_and_sort_loans(loans)
            df_html = df.head(15).to_html(index=False)
            st.title('Borrow&Return Records')
            st.write(df_html, unsafe_allow_html=True)
            st.write(f"Number of books borrowed: {len(loans)}")
            st.write(f"Number of books borrowing: {len(df[df['Status'] == 'borrowing'])}")
            st.write(f"Number of books returned: {len(df[df['Status'].isin(['returned', 'overdue returned'])])}")
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
