"""
FastAPI Book API - Complete CRUD Application
============================================

HOW TO RUN:
1. Install dependencies: pip install fastapi uvicorn
2. Run this file: python book_api.py
3. Open browser: http://localhost:8000/docs (Swagger UI)
4. Or use: uvicorn book_api:app --reload

The API will be available at http://localhost:8000
Interactive documentation at http://localhost:8000/docs
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

# ============================================================
# 1. CREATE FASTAPI APP
# ============================================================
app = FastAPI(
    title="Book Store API",
    description="CRUD API for managing books",
    version="1.0.0"
)


# ============================================================
# 2. DEFINE BOOK MODEL (RESPONSE MODEL)
# ============================================================
class Book(BaseModel):
    """
    Book response model - same structure as Item model
    
    Fields:
    - title: str (required)
    - author: str (required)
    - price: float (required)
    - is_available: bool (optional, default: None)
    - isbn: str (optional, default: None)
    """
    title: str
    author: str
    price: float
    is_available: Optional[bool] = None
    isbn: Optional[str] = None


# ============================================================
# 3. IN-MEMORY DATABASE (Sample Data)
# ============================================================
books_db = {
    1: {
        "title": "Python Programming",
        "author": "Mark Lutz",
        "price": 49.99,
        "is_available": True,
        "isbn": "978-0135802892"
    },
    2: {
        "title": "FastAPI Development",
        "author": "Sebastián Ramírez",
        "price": 39.99,
        "is_available": True,
        "isbn": "978-0134853987"
    },
    3: {
        "title": "Data Science with Python",
        "author": "Jake VanderPlas",
        "price": 55.99,
        "is_available": False,
        "isbn": "978-1491957662"
    }
}


# ============================================================
# 4. API ENDPOINTS (CRUD OPERATIONS)
# ============================================================

@app.get("/")
def read_root():
    """
    Root endpoint - Welcome message
    """
    return {
        "message": "Welcome to Book Store API",
        "docs": "Visit http://localhost:8000/docs for interactive documentation"
    }


@app.get("/books/", response_model=list[Book])
def get_all_books():
    """
    GET ALL BOOKS - Returns list of all Book objects
    
    Returns:
        List of Book objects
    """
    return [Book(**book_data) for book_data in books_db.values()]


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, q: Optional[str] = None):
    """
    GET BOOK BY ID - Returns a single Book object
    
    Parameters:
    - book_id: int (path parameter)
    - q: Optional query parameter for additional filtering
    
    Returns:
        Book object if found, else error message
    """
    if book_id in books_db:
        book_data = books_db[book_id]
        # Create Book object and return it
        book_obj = Book(**book_data)
        return book_obj
    
    return {"error": f"Book with ID {book_id} not found"}


@app.post("/books/", response_model=Book)
def create_book(book: Book):
    """
    CREATE NEW BOOK - Takes Book object as input, stores it, returns the Book object
    
    Request Body:
        {
            "title": "string",
            "author": "string",
            "price": float,
            "is_available": bool (optional),
            "isbn": "string" (optional)
        }
    
    Returns:
        The created Book object
    
    Example:
        POST /books/
        {
            "title": "Web Development with FastAPI",
            "author": "John Doe",
            "price": 45.50,
            "is_available": true,
            "isbn": "978-0123456789"
        }
    """
    # Get next available ID
    new_id = max(books_db.keys()) + 1 if books_db else 1
    
    # Store book data in database
    books_db[new_id] = book.model_dump()
    
    print(f"✓ Book created with ID {new_id}: {book.title}")
    
    # Return the Book object
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    """
    UPDATE EXISTING BOOK - Takes Book object as input, updates it, returns the updated Book object
    
    Parameters:
    - book_id: int (path parameter)
    
    Request Body:
        {
            "title": "string",
            "author": "string",
            "price": float,
            "is_available": bool (optional),
            "isbn": "string" (optional)
        }
    
    Returns:
        The updated Book object if found, else error message
    
    Example:
        PUT /books/1
        {
            "title": "Advanced Python Programming",
            "author": "Mark Lutz",
            "price": 59.99,
            "is_available": false,
            "isbn": "978-0135802892"
        }
    """
    if book_id in books_db:
        # Update the book data in database
        books_db[book_id] = book.model_dump()
        
        print(f"✓ Book updated with ID {book_id}: {book.title}")
        
        # Return the updated Book object
        return book
    
    return {"error": f"Book with ID {book_id} not found"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """
    DELETE BOOK - Deletes a book and returns the deleted Book object
    
    Parameters:
    - book_id: int (path parameter)
    
    Returns:
        Deleted Book object if found, else error message
    
    Example:
        DELETE /books/1
    """
    if book_id in books_db:
        # Remove book from database and get its data
        deleted_book_data = books_db.pop(book_id)
        
        # Create Book object from deleted data
        deleted_book = Book(**deleted_book_data)
        
        print(f"✓ Book deleted with ID {book_id}: {deleted_book.title}")
        
        # Return the deleted Book object with success message
        return {
            "message": f"Book with ID {book_id} deleted successfully",
            "book": deleted_book
        }
    
    return {"error": f"Book with ID {book_id} not found"}


# ============================================================
# 5. RUN THE APPLICATION
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Book Store API...")
    print("=" * 60)
    print("\n📖 Available Endpoints:")
    print("   GET    /              - Welcome message")
    print("   GET    /books/        - Get all books")
    print("   GET    /books/{id}    - Get book by ID")
    print("   POST   /books/        - Create new book")
    print("   PUT    /books/{id}    - Update book")
    print("   DELETE /books/{id}    - Delete book")
    print("\n📚 Sample Data: 3 books loaded")
    print("\n🌐 Open in browser: http://localhost:8000")
    print("📖 Interactive Docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")
    
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)