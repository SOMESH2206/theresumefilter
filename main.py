from app import app
import webbrowser
import threading

def open_browser():
    """Opens the default web browser after the server starts."""
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start() 
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
