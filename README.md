# 📚 BookNest - Personal Library Manager

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

A professional, feature-rich personal library management application built with Streamlit. BookNest helps you organize your book collection, track reading progress, and visualize your reading habits.

![BookNest](https://img.shields.io/badge/BookNest-1.0.0-205781)

## 🌟 Features

- **Book Management**
  - Add, view, and remove books from your collection
  - Track reading progress for books in progress
  - Categorize books by genre and reading status

- **Smart Search**
  - Find books quickly by title or author
  - Filter your collection based on various criteria

- **Reading Statistics**
  - Visualize your reading habits with interactive charts
  - Track genre distribution and reading progress
  - Monitor monthly reading activity

- **Personalized Recommendations**
  - Get book recommendations based on your reading patterns
  - Discover new authors in your favorite genres

- **Data Management**
  - Auto-save functionality to prevent data loss
  - Export your library to CSV format

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal_library_manager.git
   cd personal_library_manager
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

1. Start the application:
   ```bash
   streamlit run main.py
   ```

2. The application will open in your default web browser at `http://localhost:8501`

3. Navigate through the application using the sidebar:
   - **Library**: Manage your book collection
   - **Statistics**: View reading statistics and visualizations
   - **Settings**: Configure application settings and export data

## 🎨 User Interface

BookNest features a clean, intuitive interface with a professional color scheme:

- Primary: #205781
- Secondary: #4F959D
- Accent: #98D2C0
- Background: #F6F8D5

## 📊 Library Management

### Adding Books
Add books to your collection by providing:
- Title
- Author
- Genre
- Total Pages
- Reading Status (Unread, In Progress, Completed)

### Tracking Progress
For books marked as "In Progress", use the slider to update your reading progress. The application automatically calculates and visualizes your overall reading statistics.

### View Options
Toggle between List View and Grid View to display your collection in your preferred format.

## 🔄 Data Persistence

BookNest automatically saves your library data every 30 seconds to prevent data loss. You can also manually save your library at any time using the "Save Library" button in the sidebar.

## 🛠️ Technical Details

- **Framework**: Streamlit
- **Data Storage**: JSON
- **Visualization**: Matplotlib
- **Data Processing**: Pandas

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Developed with ❤️ for book lovers everywhere.