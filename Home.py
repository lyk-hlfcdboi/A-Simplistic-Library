import streamlit as st
from Pages import user_auth, search_book, borrow_return, account_management

def main():
    initialize_session_state()
    render_sidebar_menu()
    process_page_navigation()

def initialize_session_state():
    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = 'no log'

    if 'choice' not in st.session_state:
        st.session_state['choice'] = "Search Books"
    else: 
        return
    if 'redirect_to' not in st.session_state:
        st.session_state['redirect_to'] = None

def render_sidebar_menu():
    st.sidebar.title("Menu")
    menu_options = ["Search Books", "Login/Signup", "Borrow/Return Books", "Account Management"]
    # Ensure 'choice' is a valid option; otherwise, reset it
    if st.session_state['choice'] not in menu_options:
        st.session_state['choice'] = "Search Books"
    current_choice_index = menu_options.index(st.session_state['choice'])
    st.session_state['choice'] = st.sidebar.selectbox('', menu_options, index=current_choice_index)

def process_page_navigation():
    if st.session_state['choice'] == "Search Books":
        search_book.render_search_page()
    elif st.session_state['choice'] == "Login/Signup":
        process_login_signup()
    elif st.session_state['choice'] == "Borrow/Return Books":
        process_borrow_return()
    elif st.session_state['choice'] == "Account Management":
        process_account_management()

def process_login_signup():
    login_result = user_auth.render_login_signup()  # Placeholder function
    if login_result and len(login_result) == 6:  # Successful login
        st.session_state['login_status'] = 'LS'
        st.session_state['userid'] = login_result
        redirect_post_login()
    else:  # Login failed or canceled
        pass
        #st.error("Login failed. Please try again.")

def process_borrow_return():
    if require_login():
        borrow_return.borrow_return_page()

def process_account_management():
    if require_login():
        account_management.account_management_page()

def require_login():
    """Redirect to Login/Signup if not logged in. Return True if already logged in."""
    if st.session_state['login_status'] == 'no log':
        st.session_state['redirect_to'] = st.session_state['choice']
        st.session_state['choice'] = "Login/Signup"
        st.experimental_rerun()
    return True

def redirect_post_login():
    """Redirects to a previously attempted page or defaults after login."""
    if st.session_state['redirect_to'] == None:
        st.session_state['choice'] = 'Borrow/Return Books'
        return
    st.session_state['choice'] = st.session_state['redirect_to']
    st.session_state['redirect_to'] = None
    st.experimental_rerun()

if __name__ == "__main__":
    main()


