"""Flask API for the Algorithm Visualizer project."""

import os
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.get("/")
def home():
    """Return a small response to confirm that the API is running."""
    return jsonify(message="Algorithm Visualizer API is running")


@app.get("/api/status")
def api_status():
    """Provide a simple endpoint for checking backend health."""
    return jsonify(status="success", message="Backend is working")


@app.post("/api/bubble-sort")
def bubble_sort():
    """Run the C Bubble Sort program and return its result."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Request body must be a JSON object."), 400

    array = data.get("array")

    if not isinstance(array, list):
        return jsonify(error="'array' must be a list."), 400

    if not all(isinstance(value, int) and not isinstance(value, bool)
               for value in array):
        return jsonify(error="'array' must contain integers only."), 400

    if not 1 <= len(array) <= 1000:
        return jsonify(
            error="Array size must be between 1 and 1000."
        ), 400

    # Locate bubble_sort.exe.
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    c_program = os.path.join(
        project_root,
        "c_engine",
        "bubble_sort.exe"
    )

    if not os.path.exists(c_program):
        return jsonify(
            error="bubble_sort.exe was not found."
        ), 500

    # Input sent to C.
    c_input = f"{len(array)}\n{' '.join(map(str, array))}\n"

    try:
        result = subprocess.run(
            [c_program],
            input=c_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify(error="C program timed out."), 500
    except OSError as error:
        return jsonify(
            error=f"Could not run C program: {error}"
        ), 500

    if result.returncode != 0:
        return jsonify(
            error="C Bubble Sort program failed.",
            details=result.stderr.strip()
        ), 500

    # Read C output.
    output_lines = result.stdout.strip().splitlines()
    print("DEBUG C OUTPUT:", repr(result.stdout))

    sorted_array = None
    comparisons = None
    swaps = None
    steps = []

    for line in output_lines:
        line = line.strip()

        if line.startswith("STEP:"):
            parts = line.split(":")

            if len(parts) == 4:
                step_type = parts[1].lower()
                index1 = int(parts[2])
                index2 = int(parts[3])

                steps.append({
                    "type": step_type,
                    "index1": index1,
                    "index2": index2,
            })

        elif line.startswith("SORTED:"):
            numbers = line.replace("SORTED:", "", 1).strip()

            if numbers:
                sorted_array = [int(value) for value in numbers.split()]
            else:
                sorted_array = []

        elif line.startswith("COMPARISONS:"):
            comparisons = int(
            line.replace("COMPARISONS:", "", 1).strip()
        )

        elif line.startswith("SWAPS:"):
            swaps = int(
            line.replace("SWAPS:", "", 1).strip()
        )
    if sorted_array is None or comparisons is None or swaps is None:
        return jsonify(
            error="Unexpected output from C Bubble Sort program.",
            c_output=result.stdout
        ), 500

    return jsonify(
        algorithm="Bubble Sort",
        sorted_array=sorted_array,
        comparisons=comparisons,
        swaps=swaps,
        steps=steps
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )