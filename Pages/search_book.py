import streamlit as st
import requests
import pandas as pd

# Function to perform the search
def search_books(book_title, author_name):
    # Firebase Database URL
    db_url = 'https://library551-default-rtdb.firebaseio.com/Book.json'
    results = {}; 

    # Search by Book Title (Exact Match)
    if book_title:
        query = f'orderBy="title"&equalTo="{book_title}"'
        response = requests.get(f'{db_url}?{query}')
        books = response.json().items()
        for book_id, info in books.items():
            results[book_id] = info


    # Search by Author (Exact and Contains)
    if author_name:
        query = f'orderBy="title"&equalTo="{author_name}"'
        response = requests.get(f'{db_url}?{query}')
        for book_id, book_info in books.items():
            if author_name in book_info.get("author", []):  # Checks if author_name is in the authors list
                results[book_id] =  book_info

    return results

def render_search_page():
    st.title("Search Books")

    # Input bars for search criteria
    book_title = st.text_input("Input the book title", "")
    author_name = st.text_input("Input the author", "")

    # Search button
    if st.button('Search'):
        # Perform the search
        search_results = search_books(book_title, author_name)

        if search_results:
            data = []
            
            # Process and display results in a table
            for book_id, info in search_results:
                print(info)
                d_ = {
                    "ID": book_id,
                    "Title": info["title"],
                    "Authors": ", ".join(info.get("authors", [])),
                    "Genres": ", ".join(info.get("subjects", [])),
                    "In Stock": info.get("availableNums", 0)
                }
                data.append(d_)

            df = pd.DataFrame(data)
            df.reset_index(drop = True, inplace = True)
            st.table(df)
        else:
            st.error("Your book is not found.")


if __name__ == "__main__":
    render_search_page()
