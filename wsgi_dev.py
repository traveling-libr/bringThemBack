"""
wsgi entry point
This module serves as the entry point to this application.
"""
from app import app

# Start the development server
if __name__ == "__main__":
    app.run(debug=True)