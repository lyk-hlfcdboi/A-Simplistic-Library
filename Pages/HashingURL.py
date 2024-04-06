bookURLS = {
    0: "https://books-1-25ca2-default-rtdb.firebaseio.com/books",
    1: "https://books-2-87c03-default-rtdb.firebaseio.com/books",
    2: "https://books-3-82c7c-default-rtdb.firebaseio.com/books",
    3: "https://books-4-b4971-default-rtdb.firebaseio.com/books",
    4: "https://books-5-20414-default-rtdb.firebaseio.com/books"
}

userURLS = {
    0: "https://user-1-9306f-default-rtdb.firebaseio.com/users",
    1: "https://user-2-40a0a-default-rtdb.firebaseio.com/users"
}

def get_book_path(i):
	getURL = bookURLS[i]
	return getURL

def get_user_path(i):
	getURL = userURLS[i]
	return getURL

def hash_book(isbn):
    return isbn%5

def hash_user(userID):
    return userID%2
