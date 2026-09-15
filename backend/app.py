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
@app.post("/api/selection-sort")
def selection_sort():
    """Run the C Selection Sort program and return its result."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            error="Request body must be a JSON object."
        ), 400

    array = data.get("array")

    if not isinstance(array, list):
        return jsonify(
            error="'array' must be a list."
        ), 400

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in array
    ):
        return jsonify(
            error="'array' must contain integers only."
        ), 400

    if not 1 <= len(array) <= 1000:
        return jsonify(
            error="Array size must be between 1 and 1000."
        ), 400

    # Locate selection_sort.exe.
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    c_program = os.path.join(
        project_root,
        "c_engine",
        "selection_sort.exe"
    )

    if not os.path.exists(c_program):
        return jsonify(
            error="selection_sort.exe was not found."
        ), 500

    # Input sent to C.
    c_input = (
        f"{len(array)}\n"
        f"{' '.join(map(str, array))}\n"
    )

    try:
        result = subprocess.run(
            [c_program],
            input=c_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify(
            error="C program timed out."
        ), 500
    except OSError as error:
        return jsonify(
            error=f"Could not run C program: {error}"
        ), 500

    if result.returncode != 0:
        return jsonify(
            error="C Selection Sort program failed.",
            details=result.stderr.strip()
        ), 500

    # Read C output.
    output_lines = result.stdout.strip().splitlines()

    print("DEBUG C SELECTION OUTPUT:", repr(result.stdout))

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
            numbers = line.replace(
                "SORTED:",
                "",
                1
            ).strip()

            if numbers:
                sorted_array = [
                    int(value)
                    for value in numbers.split()
                ]
            else:
                sorted_array = []

        elif line.startswith("COMPARISONS:"):
            comparisons = int(
                line.replace(
                    "COMPARISONS:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("SWAPS:"):
            swaps = int(
                line.replace(
                    "SWAPS:",
                    "",
                    1
                ).strip()
            )

    if (
        sorted_array is None
        or comparisons is None
        or swaps is None
    ):
        return jsonify(
            error="Unexpected output from C Selection Sort program.",
            c_output=result.stdout
        ), 500

    return jsonify(
        algorithm="Selection Sort",
        sorted_array=sorted_array,
        comparisons=comparisons,
        swaps=swaps,
        steps=steps
    )
@app.post("/api/insertion-sort")
def insertion_sort():
    """Run the C Insertion Sort program and return its result."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            error="Request body must be a JSON object."
        ), 400

    array = data.get("array")

    if not isinstance(array, list):
        return jsonify(
            error="'array' must be a list."
        ), 400

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in array
    ):
        return jsonify(
            error="'array' must contain integers only."
        ), 400

    if not 1 <= len(array) <= 1000:
        return jsonify(
            error="Array size must be between 1 and 1000."
        ), 400

    # Locate insertion_sort.exe.
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    c_program = os.path.join(
        project_root,
        "c_engine",
        "insertion_sort.exe"
    )

    if not os.path.exists(c_program):
        return jsonify(
            error="insertion_sort.exe was not found."
        ), 500

    # Input sent to C.
    c_input = (
        f"{len(array)}\n"
        f"{' '.join(map(str, array))}\n"
    )

    try:
        result = subprocess.run(
            [c_program],
            input=c_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify(
            error="C program timed out."
        ), 500
    except OSError as error:
        return jsonify(
            error=f"Could not run C program: {error}"
        ), 500

    if result.returncode != 0:
        return jsonify(
            error="C Insertion Sort program failed.",
            details=result.stderr.strip()
        ), 500

    # Read C output.
    output_lines = result.stdout.strip().splitlines()

    print(
        "DEBUG C INSERTION OUTPUT:",
        repr(result.stdout)
    )

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
            numbers = line.replace(
                "SORTED:",
                "",
                1
            ).strip()

            if numbers:
                sorted_array = [
                    int(value)
                    for value in numbers.split()
                ]
            else:
                sorted_array = []

        elif line.startswith("COMPARISONS:"):
            comparisons = int(
                line.replace(
                    "COMPARISONS:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("SWAPS:"):
            swaps = int(
                line.replace(
                    "SWAPS:",
                    "",
                    1
                ).strip()
            )

    if (
        sorted_array is None
        or comparisons is None
        or swaps is None
    ):
        return jsonify(
            error="Unexpected output from C Insertion Sort program.",
            c_output=result.stdout
        ), 500

    return jsonify(
        algorithm="Insertion Sort",
        sorted_array=sorted_array,
        comparisons=comparisons,
        swaps=swaps,
        steps=steps
    )
@app.post("/api/merge-sort")
def merge_sort():
    """Run the C Merge Sort program and return its result."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            error="Request body must be a JSON object."
        ), 400

    array = data.get("array")

    if not isinstance(array, list):
        return jsonify(
            error="'array' must be a list."
        ), 400

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in array
    ):
        return jsonify(
            error="'array' must contain integers only."
        ), 400

    if not 1 <= len(array) <= 1000:
        return jsonify(
            error="Array size must be between 1 and 1000."
        ), 400

    # Locate merge_sort.exe.
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    c_program = os.path.join(
        project_root,
        "c_engine",
        "merge_sort.exe"
    )

    if not os.path.exists(c_program):
        return jsonify(
            error="merge_sort.exe was not found."
        ), 500

    # Input sent to C.
    c_input = (
        f"{len(array)}\n"
        f"{' '.join(map(str, array))}\n"
    )

    try:
        result = subprocess.run(
            [c_program],
            input=c_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify(
            error="C program timed out."
        ), 500
    except OSError as error:
        return jsonify(
            error=f"Could not run C program: {error}"
        ), 500

    if result.returncode != 0:
        return jsonify(
            error="C Merge Sort program failed.",
            details=result.stderr.strip()
        ), 500

    # Read C output.
    output_lines = result.stdout.strip().splitlines()

    print(
        "DEBUG C MERGE OUTPUT:",
        repr(result.stdout)
    )

    sorted_array = None
    comparisons = None
    writes = None
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
            numbers = line.replace(
                "SORTED:",
                "",
                1
            ).strip()

            if numbers:
                sorted_array = [
                    int(value)
                    for value in numbers.split()
                ]
            else:
                sorted_array = []

        elif line.startswith("COMPARISONS:"):
            comparisons = int(
                line.replace(
                    "COMPARISONS:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("WRITES:"):
            writes = int(
                line.replace(
                    "WRITES:",
                    "",
                    1
                ).strip()
            )

    if (
        sorted_array is None
        or comparisons is None
        or writes is None
    ):
        return jsonify(
            error="Unexpected output from C Merge Sort program.",
            c_output=result.stdout
        ), 500

    return jsonify(
        algorithm="Merge Sort",
        sorted_array=sorted_array,
        comparisons=comparisons,
        writes=writes,
        steps=steps
    )
@app.post("/api/quick-sort")
def quick_sort():
    """Run the C Quick Sort program and return its result."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            error="Request body must be a JSON object."
        ), 400

    array = data.get("array")

    if not isinstance(array, list):
        return jsonify(
            error="'array' must be a list."
        ), 400

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in array
    ):
        return jsonify(
            error="'array' must contain integers only."
        ), 400

    if not 1 <= len(array) <= 1000:
        return jsonify(
            error="Array size must be between 1 and 1000."
        ), 400

    # Locate quick_sort.exe.
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    c_program = os.path.join(
        project_root,
        "c_engine",
        "quick_sort.exe"
    )

    if not os.path.exists(c_program):
        return jsonify(
            error="quick_sort.exe was not found."
        ), 500

    # Input sent to C.
    c_input = (
        f"{len(array)}\n"
        f"{' '.join(map(str, array))}\n"
    )

    try:
        result = subprocess.run(
            [c_program],
            input=c_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify(
            error="C program timed out."
        ), 500
    except OSError as error:
        return jsonify(
            error=f"Could not run C program: {error}"
        ), 500

    if result.returncode != 0:
        return jsonify(
            error="C Quick Sort program failed.",
            details=result.stderr.strip()
        ), 500

    # Read C output.
    output_lines = result.stdout.strip().splitlines()

    print(
        "DEBUG C QUICK OUTPUT:",
        repr(result.stdout)
    )

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
            numbers = line.replace(
                "SORTED:",
                "",
                1
            ).strip()

            if numbers:
                sorted_array = [
                    int(value)
                    for value in numbers.split()
                ]
            else:
                sorted_array = []

        elif line.startswith("COMPARISONS:"):
            comparisons = int(
                line.replace(
                    "COMPARISONS:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("SWAPS:"):
            swaps = int(
                line.replace(
                    "SWAPS:",
                    "",
                    1
                ).strip()
            )

    if (
        sorted_array is None
        or comparisons is None
        or swaps is None
    ):
        return jsonify(
            error="Unexpected output from C Quick Sort program.",
            c_output=result.stdout
        ), 500

    return jsonify(
        algorithm="Quick Sort",
        sorted_array=sorted_array,
        comparisons=comparisons,
        swaps=swaps,
        steps=steps
    )
@app.post("/api/linear-search")
def linear_search():
    """Run the C Linear Search program and return its result."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            error="Request body must be a JSON object."
        ), 400

    array = data.get("array")
    target = data.get("target")

    if not isinstance(array, list):
        return jsonify(
            error="'array' must be a list."
        ), 400

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in array
    ):
        return jsonify(
            error="'array' must contain integers only."
        ), 400

    if not 1 <= len(array) <= 1000:
        return jsonify(
            error="Array size must be between 1 and 1000."
        ), 400

    if not isinstance(target, int) or isinstance(target, bool):
        return jsonify(
            error="'target' must be an integer."
        ), 400

    # Locate linear_search.exe.
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    c_program = os.path.join(
        project_root,
        "c_engine",
        "linear_search.exe"
    )

    if not os.path.exists(c_program):
        return jsonify(
            error="linear_search.exe was not found."
        ), 500

    # Input sent to C.
    c_input = (
        f"{len(array)}\n"
        f"{' '.join(map(str, array))}\n"
        f"{target}\n"
    )

    try:
        result = subprocess.run(
            [c_program],
            input=c_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify(
            error="C program timed out."
        ), 500
    except OSError as error:
        return jsonify(
            error=f"Could not run C program: {error}"
        ), 500

    if result.returncode != 0:
        return jsonify(
            error="C Linear Search program failed.",
            details=result.stderr.strip()
        ), 500

    # Read C output.
    output_lines = result.stdout.strip().splitlines()

    print(
        "DEBUG C LINEAR SEARCH OUTPUT:",
        repr(result.stdout)
    )

    found_index = None
    comparisons = None
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

        elif line.startswith("FOUND_INDEX:"):
            found_index = int(
                line.replace(
                    "FOUND_INDEX:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("COMPARISONS:"):
            comparisons = int(
                line.replace(
                    "COMPARISONS:",
                    "",
                    1
                ).strip()
            )

    if found_index is None or comparisons is None:
        return jsonify(
            error="Unexpected output from C Linear Search program.",
            c_output=result.stdout
        ), 500

    return jsonify(
        algorithm="Linear Search",
        found_index=found_index,
        target=target,
        comparisons=comparisons,
        steps=steps
    )
@app.post("/api/binary-search")
def binary_search():
    """Run the C Binary Search program and return its result."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            error="Request body must be a JSON object."
        ), 400

    array = data.get("array")
    target = data.get("target")

    if not isinstance(array, list):
        return jsonify(
            error="'array' must be a list."
        ), 400

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in array
    ):
        return jsonify(
            error="'array' must contain integers only."
        ), 400

    if not 1 <= len(array) <= 1000:
        return jsonify(
            error="Array size must be between 1 and 1000."
        ), 400

    if not isinstance(target, int) or isinstance(target, bool):
        return jsonify(
            error="'target' must be an integer."
        ), 400

    # Binary Search requires a sorted array.
    if array != sorted(array):
        return jsonify(
            error="Binary Search requires a sorted array."
        ), 400

    # Locate binary_search.exe.
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    c_program = os.path.join(
        project_root,
        "c_engine",
        "binary_search.exe"
    )

    if not os.path.exists(c_program):
        return jsonify(
            error="binary_search.exe was not found."
        ), 500

    # Input sent to C.
    c_input = (
        f"{len(array)}\n"
        f"{' '.join(map(str, array))}\n"
        f"{target}\n"
    )

    try:
        result = subprocess.run(
            [c_program],
            input=c_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify(
            error="C program timed out."
        ), 500
    except OSError as error:
        return jsonify(
            error=f"Could not run C program: {error}"
        ), 500

    if result.returncode != 0:
        return jsonify(
            error="C Binary Search program failed.",
            details=result.stderr.strip()
        ), 500

    # Read C output.
    output_lines = result.stdout.strip().splitlines()

    print(
        "DEBUG C BINARY SEARCH OUTPUT:",
        repr(result.stdout)
    )

    found_index = None
    comparisons = None
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

        elif line.startswith("FOUND_INDEX:"):
            found_index = int(
                line.replace(
                    "FOUND_INDEX:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("COMPARISONS:"):
            comparisons = int(
                line.replace(
                    "COMPARISONS:",
                    "",
                    1
                ).strip()
            )

    if found_index is None or comparisons is None:
        return jsonify(
            error="Unexpected output from C Binary Search program.",
            c_output=result.stdout
        ), 500

    return jsonify(
        algorithm="Binary Search",
        found_index=found_index,
        target=target,
        comparisons=comparisons,
        steps=steps
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )