"""A minimal Flask API for the Algorithm Visualizer project."""

from flask import Flask, jsonify


# Create the Flask application. __name__ helps Flask find this file's resources.
app = Flask(__name__)


@app.get("/")
def home():
    """Return a small response to confirm that the API is running."""
    # jsonify converts this Python dictionary into a JSON HTTP response.
    return jsonify(message="Algorithm Visualizer API is running")


@app.get("/api/status")
def api_status():
    """Provide a simple endpoint for checking backend health."""
    return jsonify(status="success", message="Backend is working")


if __name__ == "__main__":
    # Start Flask's development server at http://127.0.0.1:5000.
    # Run from the project root with: python backend/app.py
    app.run(host="127.0.0.1", port=5000, debug=True)
