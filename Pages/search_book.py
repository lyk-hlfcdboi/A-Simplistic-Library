import streamlit as st
import requests
import pandas as pd
import json
from requests.exceptions import JSONDecodeError
from Pages.HashingURL import hash_book, get_book_path
from urllib.parse import quote

def adjust_input(full_name):
	parts = full_name.split()
	adjusted_parts = [part[0].upper() + part[1:].lower() for part in parts]
	adjusted_name = " ".join(adjusted_parts)
	return adjusted_name

bookURLS = {
    0: "https://books-1-25ca2-default-rtdb.firebaseio.com/books",
    1: "https://books-2-87c03-default-rtdb.firebaseio.com/books",
    2: "https://books-3-82c7c-default-rtdb.firebaseio.com/books",
    3: "https://books-4-b4971-default-rtdb.firebaseio.com/books",
    4: "https://books-5-20414-default-rtdb.firebaseio.com/books"
}


# Function to perform the search
def search_books(book_title, author_name):
    # Firebase Database URL
    # book_title = adjust_input(book_title)
    
    results = {}; 

    # Search by Book Title (Exact Match)
    if book_title:
        query_params = {
            'orderBy': json.dumps('title'),
            'equalTo': json.dumps(book_title)
        }

        for url in bookURLS.values():
            response = requests.get(f"{url}.json", params = query_params)
            if response.status_code == 200:
                try:
                    books = response.json()
                    if books:
                        for book_id, info in books.items():
                            results[book_id] = info
                except JSONDecodeError:
                    # Handle the case where the response body isn't valid JSON
                    print(f"Invalid JSON response from {url}")
                    continue
            else:
                # Handle failed requests
                print(f"Failed to fetch data from {url}, status code: {response.status_code}")

    # Search by Author (Exact and Contains)
    author_exact = False
    if author_name:
        author_name = adjust_input(author_name)
        encode_name = quote(author_name)
        # first exact-search author name
        for url in bookURLS.values():
            response = requests.get(f"{url.strip('books')}/author/{encode_name}.json")
            if response.json():
                for bid in response.json().keys():
                    url_ = get_book_path(hash_book(int(bid)))
                    bk_resp = requests.get(f"{url_}/{bid}.json")
                    if bk_resp.status_code == 200:
                        if bk_resp.json():
                            results[bid] = bk_resp.json()
                            author_exact = True
                            print('An Exact Match Exists')

        if not author_exact:
            name_kw = author_name.split()
            # print(name_kw)
            
            for nkw in name_kw:
                for url in bookURLS.values():   
                    response = requests.get(f"{url.strip('books')}/authorKeyWord/{nkw}.json")
                    if response.status_code == 200:
                        try:
                            dict_bid = response.json()
                            if dict_bid:
                                for id_ in dict_bid.keys():
                                    url_ = get_book_path(hash_book(int(id_)))
                                    resp = requests.get(f"{url_}/{id_}.json")
                                    if resp.status_code == 200 and resp.json():
                                        results[id_] = resp.json()
                                    else:
                                        continue
                        except JSONDecodeError:
                            # Handle the case where the response body isn't valid JSON
                            print(f"Invalid JSON response from {url}")
                            continue
                    else:
                        # Handle failed requests
                        print(f"Failed to fetch data from {url}, status code: {response.status_code}")
    return results, author_exact

def render_search_page():
    st.title("Search Books")

    # Input bars for search criteria
    book_title = st.text_input("Input the book title", "")
    author_name = st.text_input("Input the author", "")

    # Search button
    if st.button('Search'):
        # Perform the search
        search_results, author_exact = search_books(book_title, author_name)
        
        if not book_title and not author_name:
            st.warning("Please enter a book title or an author name to perform the search.")
            return
        if search_results:
            data = []
            
            # Process and display results in a table
            for book_id, info in search_results.items():
                authors = info.get("authors", [])
                if authors:
                    authors = [a.replace(',', '') for a in authors.keys()] 
                subjects = info['subjects']
                d_ = {
                    "ID": book_id,
                    "Title": info["title"],
                    "Authors": ", ".join(authors),
                    "Genres": ', '.join(subjects) if isinstance(subjects, list) else subjects,
                    "In Stock": info.get("availableNums", 0)
                }
                data.append(d_)

            df = pd.DataFrame(data)
            df_html = df.head(15).to_html(index=False)
            st.title('Search Results')
            if not author_exact:
                st.write('You might be finding:')
            st.write(df_html, unsafe_allow_html=True)
        else:
            st.error("Your book is not found.")


if __name__ == "__main__":
    render_search_page()
