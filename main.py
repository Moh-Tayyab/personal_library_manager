import streamlit as st
import pandas as pd
import random
import os
import json
import matplotlib.pyplot as plt
import time

# Configure page
st.set_page_config(page_title="BookNest", page_icon="📚", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora&display=swap');
    .main {background-color: #FFF9F2;}
    h1 {color: #5E4B32; font-family: 'Lora', serif;}
    .stButton>button {background-color: #D7CEC1; color: #5E4B32;}
    .stTextInput>div>div>input {background-color: #FDF7EC;}
    .stSelectbox>div>div>select {background-color: #FDF7EC;}
    .book-card {padding: 15px; background: #FFFFFF; border-radius: 10px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

# Update CSS for professional look
st.markdown("""
<style>
    :root {
        --primary: #205781;
        --secondary: #4F959D;
        --accent: #98D2C0;
        --background: #F6F8D5;
    }
    .main {background-color: var(--background);}
    h1 {color: var(--primary); border-bottom: 2px solid var(--secondary); padding-bottom: 0.5rem;}
    .stButton>button {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .book-card {
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .metric-box {
        background: white !important;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stSelectbox, .stTextInput, .stNumberInput {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
    }
    .book-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Data persistence functions
def save_books():
    """Save books to JSON file"""
    with open('d:/personal_library_manager/books_data.json', 'w') as f:
        json.dump(st.session_state.books, f)
    
def load_books():
    """Load books from JSON file"""
    try:
        with open('d:/personal_library_manager/books_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Initialize session state
if 'books' not in st.session_state:
    st.session_state.books = load_books()
    
if 'last_save_time' not in st.session_state:
    st.session_state.last_save_time = time.time()

# Helper functions
def generate_recommendations():
    genres = [book['genre'] for book in st.session_state.books]
    if genres:
        top_genres = pd.Series(genres).value_counts().index[:2]
        return [f"{genre} Masterpieces" for genre in top_genres]
    return ["Classic Literature", "Modern Fantasy"]

def auto_save():
    """Auto-save if 30 seconds have passed since last save"""
    current_time = time.time()
    if current_time - st.session_state.last_save_time > 30:
        save_books()
        st.session_state.last_save_time = current_time

# Sidebar Navigation
with st.sidebar:
    st.title("📚 BookNest")
    st.markdown("---")
    
    nav = st.radio("Navigation", ["Library", "Statistics", "Settings"])
    
    st.markdown("---")
    if st.button("💾 Save Library"):
        save_books()
        st.success("Library saved successfully!")
    
    st.markdown("---")
    st.caption("Your library auto-saves every 30 seconds")

# Header Section
st.title("📖Your Personal Library")

# Main content based on navigation
if nav == "Library":
    # Main Dashboard Columns
    col1, col2, col3 = st.columns([3,2,2])

    # === Book Management Column ===
    with col1:
        st.subheader("Manage Your Collection")
        
        with st.expander("➕ Add New Book", expanded=True):
            with st.form("add_book"):
                title = st.text_input("Title")
                author = st.text_input("Author")
                genre = st.text_input("Genre", placeholder="Enter book genre (e.g., Fiction, Fantasy, Mystery)")
                pages = st.number_input("Total Pages", min_value=1)
                status = st.selectbox("Reading Status", ["Unread", "In Progress", "Completed"])
                
                if st.form_submit_button("Add to Library"):
                    if any(b['title'].lower() == title.lower() and b['author'].lower() == author.lower() 
                        for b in st.session_state.books):
                        st.error("📚 Twin books detected! This title already exists in your library!")
                    else:
                        st.session_state.books.append({
                            'title': title,
                            'author': author,
                            'genre': genre,
                            'pages': pages,
                            'status': status,
                            'pages_read': 0
                        })
                        save_books()  # Save immediately on add
                        st.success("Book added to your cozy collection!")

    # === Delete & Search Column ===
    with col2:
        st.subheader("Curate Your Space")
        
        if st.session_state.books:
            delete_book = st.selectbox("Select Book to Remove", 
                                    [f"{b['title']} by {b['author']}" for b in st.session_state.books])
            if st.button("🚫 No Regrets Delete", help="Permanently remove from library"):
                index = [f"{b['title']} by {b['author']}" for b in st.session_state.books].index(delete_book)
                st.session_state.books.pop(index)
                save_books()  # Save immediately on delete
                st.rerun()
        
        st.subheader("Search Your Library")
        search_term = st.text_input("Search by title or author")
        search_results = [b for b in st.session_state.books 
                        if search_term.lower() in b['title'].lower() or 
                        search_term.lower() in b['author'].lower()]

    # === Reading Progress Column ===
    with col3:
        st.subheader("Reading Journey")
        
        status_counts = {'Unread':0, 'In Progress':0, 'Completed':0}
        for book in st.session_state.books:
            status_counts[book['status']] += 1
        
        st.metric("Unread Books", status_counts['Unread'])
        st.metric("Books in Progress", status_counts['In Progress'])
        st.metric("Completed Books", status_counts['Completed'])

    # === Book Display Section with Grid View ===
    st.divider()
    st.subheader("Your Literary Collection")
    
    display_mode = st.radio("Display Mode", ["List View", "Grid View"], horizontal=True)
    
    # If search term is empty, show all books, otherwise show search results
    display_books = st.session_state.books if not search_term else search_results
    
    if display_books:
        if display_mode == "Grid View":
            # Grid View
            st.markdown('<div class="book-grid fade-in">', unsafe_allow_html=True)
            grid_cols = st.columns(3)
            for i, book in enumerate(search_results):
                with grid_cols[i % 3]:
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{book['title']}</h3>
                        <p>by {book['author']}</p>
                        <p>{book['genre']} • {book['pages']} pages</p>
                        <p>Status: {book['status']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if book['status'] == "In Progress":
                        progress = st.slider("Reading Progress", 0, book['pages'], book['pages_read'], 
                                        key=f"grid_progress_{book['title']}")
                        book['pages_read'] = progress
                        save_books()  # Save on progress update
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # List View (original)
            for book in search_results:
                with st.container():
                    cols = st.columns([3,1,2])
                    with cols[0]:
                        st.markdown(f"**{book['title']}** by {book['author']}")  
                        st.caption(f"{book['genre']} • {book['pages']} pages")
                        
                    with cols[1]:
                        status_icon = "📖" if book['status'] == "In Progress" else "✅" if book['status'] == "Completed" else "📌"
                        st.markdown(f"<h3 style='text-align: center;'>{status_icon}</h3>", unsafe_allow_html=True)
                        
                    with cols[2]:
                        if book['status'] == "In Progress":
                            progress = st.slider("Reading Progress", 0, book['pages'], book['pages_read'], 
                                            key=f"progress_{book['title']}")
                            book['pages_read'] = progress
                            save_books()  # Save on progress update
                        elif book['status'] == "Completed":
                            st.success("Fully completed! 🎉")
                        else:
                            st.info("Waiting to be explored ✨")

    # === Recommendations Section ===
    st.divider()
    st.subheader("Your Next Great Read")

    rec_cols = st.columns(3)
    recommendations = generate_recommendations()
    for i, rec in enumerate(recommendations):
        with rec_cols[i]:
            st.markdown(f"""
            <div class='book-card fade-in'>
                <h4>✨ {rec}</h4>
                <p>Curated based on your reading patterns</p>
                <small>Suggested authors: {random.choice(['Neil Gaiman', 'Jane Austen', 'Brandon Sanderson'])}</small>
            </div>
            """, unsafe_allow_html=True)

elif nav == "Statistics":
    st.header("Reading Statistics")
    
    if not st.session_state.books:
        st.info("Add some books to see your reading statistics!")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution
            st.subheader("Genre Distribution")
            genres = [book['genre'] for book in st.session_state.books]
            genre_counts = pd.Series(genres).value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', 
                   startangle=90, shadow=True)
            ax.axis('equal')
            st.pyplot(fig)
        
        with col2:
            # Reading progress
            st.subheader("Reading Progress")
            total_pages = sum(book['pages'] for book in st.session_state.books)
            read_pages = sum(book['pages_read'] for book in st.session_state.books if book['status'] == "In Progress") + \
                         sum(book['pages'] for book in st.session_state.books if book['status'] == "Completed")
            
            if total_pages > 0:
                progress_pct = (read_pages / total_pages) * 100
                st.progress(progress_pct / 100)
                st.write(f"You've read {read_pages} out of {total_pages} pages ({progress_pct:.1f}%)")
            
            # Reading status breakdown
            status_counts = {'Unread': 0, 'In Progress': 0, 'Completed': 0}
            for book in st.session_state.books:
                status_counts[book['status']] += 1
            
            fig, ax = plt.subplots()
            ax.bar(list(status_counts.keys()), list(status_counts.values()), color=['#FF9999', '#66B2FF', '#99FF99'])
            st.pyplot(fig)
        
        # Reading history (simulated)
        st.subheader("Monthly Reading Activity")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        books_read = [random.randint(1, 5) for _ in range(6)]
        
        fig, ax = plt.subplots()
        ax.plot(months, books_read, marker='o')
        ax.set_ylabel('Books Completed')
        st.pyplot(fig)

elif nav == "Settings":
    st.header("Library Settings")
    
    if st.button("Export Library as CSV"):
        df = pd.DataFrame(st.session_state.books)
        df.to_csv('d:/personal_library_manager/library_export.csv', index=False)
        st.success("Library exported to CSV!")
    
    if st.button("Clear Library"):
        confirm = st.checkbox("I understand this will delete all my books")
        if confirm:
            st.session_state.books = []
            save_books()
            st.success("Library cleared successfully!")
            st.rerun()

# Auto-save check
auto_save()