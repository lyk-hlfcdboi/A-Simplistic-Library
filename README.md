# A Simplistic Library System

This is a very simple library system built on Firebase REST API and Streamlit as the framework.

## Notes
- Due to Firebase REST API's limited query functions, you are always expected to strictly obey the upper and lower cases when typing either the titles or authors you are searching for.
- Never refresh the page after login, or you will have to log in again, but your records will be saved.
- Sometimes you might have to click the button twice to go to the page or functions you desired.

## Home Page
The main feature of this app on the home page is search. On the upper left corner, click the arrow to unwind the menu to see the full functions of this website.

### Search Book
You can search without having an account. You can search by either the full name or partial names of the author (strictly obeying upper and lower cases) or the exact title of the book.

#### By Titles
When searching by titles, an exact title is always expected, as we tried to realize exact query here. For instance:
- To search for the book 'Oliver Twist', please enter exactly 'Oliver Twist', with no space except in the middle.

#### By Authors
A part or a full name of one or several authors can be entered here, still strictly obeying the spelling. For instance:
- To search for the books authored by 'Charles Dickens', you might use one of the following ways to find it. Enter 'Charles Dickens' or 'Charles' or 'Dickens'. If a part of the name like 'Dickens' is entered, it returns all the books authored by people with the input in their names.
- To retrieve several books with different authors or a book with multiple authors, just enter part of their names and use spaces to separate them. If you want to search a book authored by Sam Smith and John Cena, you can enter any combinations of their names, like 'John Sam', 'Smith Cena', etc.

The retrieved books are presented in a table. If you want to borrow, first copy their ISBN (first column) and then check if the stock (last column) is not 0.

### Login/Signup
If you do not have an account, directly input any username and password you like, click signup, and look for the green message to confirm. If you already have an account, enter the username and password and hit login.

### Borrow/Return Book
If you directly click it without logging in, you will be redirected to the login/signup. After login, you will be automatically redirected back. In this page, there are two buttons:

#### Borrow
Enter the exact ISBN of the book you want, without spaces on the head and end; then choose the number of days you want to borrow (1 to 14), and click confirm to borrow. You can check the records in 'Account Management'.

#### Return
When returning, still enter the exact ISBN of the book you want to return. The app searches for your earliest loan record of this book.

### Account Management
You have to log in to access this page. Here, you will see the latest 15 borrow and return records and some other stats made by yourself, with start and due dates to inform a timely return. If you return a book overdue, you can expect a warning when returning it.

When you borrow or return a book, you can always come back to check the updates.
