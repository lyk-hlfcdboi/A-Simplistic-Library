import streamlit as st
import requests
from Pages.HashingURL import hash_user, get_user_path
import random
import json

# Configuration for Firebase
userURLS = {
    0: "https://user-1-9306f-default-rtdb.firebaseio.com/users",
    1: "https://user-2-40a0a-default-rtdb.firebaseio.com/users"
}

def find_username_across(username):
    query = {
    'orderBy': json.dumps("user_name"),
    'equalTo': json.dumps(username)}
    for url in userURLS.values():
        resp = requests.get(f'{url}.json', params = query)
        if resp.json():
            return resp
    return resp

def generateID():
    res = ''
    check = 'uncheck'
    while res == "000000" or res == "000001" or check:
        res = ''.join(str(random.randint(0, 9)) for _ in range(6))
        check = requests.get(f'{get_user_path(hash_user(int(res)))}/{res}.json').json()
    return res

def create_account(username, password):
    """Create a new user account in Firebase."""
    
    if username == '' or password == '' or (username.isspace() or password.isspace()):
        st.error('Please enter your userid and password.')
        return 
    
    query = {
    'orderBy': json.dumps("user_name"),
    'equalTo': json.dumps(username)}
    for url in userURLS.values():
        user_data = requests.get(f'{url}.json', params = query).json()
        if user_data:
            st.error(f'This userid already exists. Please try another.')
            return
        
    # Create new user
    userid = generateID(); 
    FIREBASE_URL = get_user_path(hash_user(int(userid)))
    data = {
            "password": password,
            "user_name": username, 
            "books": {"NoBorrowedBook": True}}
    
    response = requests.put(f"{FIREBASE_URL}/{userid}.json", json = data)
    if response.status_code == 200:
        st.success('Account created successfully.')
        return userid
    else:
        st.error('Failed to create account. Please try again.')
        #return 

def login(username, password):
    """Log in a user."""
    if username == '' or password == '' or (username.isspace() or password.isspace()):
        st.error('Please enter your userid and password.')
        return 'Error'
    response = find_username_across(username)
    if response.status_code == 200:
        if not response.json():
            st.error('Sorry, username error.')
            return 'ne'
        user_data = [i for i in response.json().values()][0]

        if user_data['password'] == password:
            return [i for i in response.json().keys()][0]
        else:
            return 'p'
    else:
        return 'No'

# The function to render the login/signup form
def render_login_signup():
    with st.form("user_auth"):
        user_name = st.text_input("UserName")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        signup_button = st.form_submit_button("Signup")
        
        if login_button:
            resp = login(user_name, password)
            if len(resp) == 6:
                # If 6-digit userid returns, login is successful
                st.success("Login Successful!")
                # You can now redirect the user or show them the main content
            elif resp == 'p':
                st.error("Wrong Password.")
            elif resp == 'ne':
                st.error("User does not exist.")
            elif resp == 'No':
                st.error("Server error, please try again later.")
            return resp
                
        elif signup_button:
            userid = create_account(user_name, password)
            if userid:
                return userid
            else:
                return 'Error'
        else: 
            pass





                
