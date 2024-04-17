# A Simplistic Library System

This is a simple library system built on Firebase REST API and Streamlit as the framework.

## 0 Notes
- Due to Firebase REST API's limited query functions, you are always expected to strictly obey the upper and lower cases to have a quick search for the results. But we do have approximate search for the author names.
- Never refresh the page after login, or you will have to log in again, but your records will be saved.
- Sometimes you might have to click the button twice to go to the page or functions you desired.

## 1 Home Page
The main feature of this app on the home page is search. On the upper left corner, click the arrow to unwind the menu to see the full functions of this website.

### 2 Search Book
You can search without having an account. You can search by either the full name or partial names of the author (strictly obeying upper and lower cases) or the exact title of the book.

#### 2.1 By Titles
When searching by titles, an exact title is always expected, as we tried to realize exact query here. For instance:
- To search for the book 'Oliver Twist', please enter exactly 'Oliver Twist', with no space except in the middle.

#### 2.2 By Authors
We achieved approximate search by creating standalone index tables for the full-name and keywords of authors' names (a part of the name).
When searching by authors, regardless of the lower/upper cases, you can input the full name of an author, or a part of the name. Either way, you can get your results if the keywords exists in the database.
For instance, to search the books by 'Clive Baker', you can either input the exact full name 'Clive Baker', even 'Clive bAkeR', or just 'Clive' or 'baker' to secure all the potential results. When you correctly enter the fll name, an exact search will be launched. If your enter does not match with any full name but matches any part of the name, a message 'You might be finding:' will lead the result, indicating you are having a approximate search.

### 3 Login/Signup
If you do not have an account, directly input any username and password you like, click signup, and look for the green message to confirm. If you already have an account, enter the username and password and hit login.

### 4 Borrow/Return Book
If you directly click it without logging in, you will be redirected to the login/signup. After login, you will be automatically redirected back. In this page, there are two buttons:

#### 4.1Borrow
Enter the exact ISBN of the book you want, without spaces on the head and end; then choose the number of days you want to borrow (1 to 14), and click confirm to borrow. You can check the records in 'Account Management'.

#### 4.2 Return
When returning, still enter the exact ISBN of the book you want to return. The app searches for your earliest loan record of this book.

### 5 Account Management
You have to log in to access this page. Here, you will see the latest 15 borrowing books of yours and their status.

When you borrow or return a book, you can always come back to check the updates.
