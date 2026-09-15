# Algorithm Visualizer

An interactive algorithm visualization platform built with HTML, CSS, JavaScript, Python, Flask, and C. It helps users understand how sorting and searching algorithms work by visualizing each step and showing key statistics in real time.

## Overview

This project combines a browser-based frontend with a Flask API and native C executables to animate algorithm execution. The frontend collects the user’s input, sends it to the backend, and then visualizes the results returned by the C engine.

## Features

- Visualize common sorting algorithms
- Visualize searching algorithms
- User-defined array input
- Random array generation
- Search target input for search algorithms
- Step-by-step execution animation
- Adjustable animation speed
- Comparison statistics
- Swap, shift, write, and found-index tracking
- Best, average, and worst-case time complexity display
- Reset and replay support
- Interactive frontend controls
- C-based algorithm execution through a Flask backend

## Tech Stack

- HTML
- CSS
- JavaScript
- Python
- Flask
- C
- Git & GitHub

## Algorithms

### Sorting Algorithms

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort

### Searching Algorithms

- Linear Search
- Binary Search

## Architecture

The application follows a simple three-layer architecture:

```text
User
  ↓
Frontend (HTML / CSS / JavaScript)
  ↓
Flask REST API
  ↓
C Algorithm Engine
  ↓
Algorithm Steps + Statistics
  ↓
Frontend Visualization
```

The frontend sends the selected array and algorithm information to the Flask backend. Flask then executes the corresponding C program, parses the output, and returns the algorithm steps and statistics to the frontend for visualization.

## Project Structure

```text
algorithm-visualizer/
├── README.md
├── .gitignore
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── app.py
│   └── requirements.txt
├── c_engine/
    ├── bubble_sort.c
    ├── selection_sort.c
    ├── insertion_sort.c
    ├── merge_sort.c
    ├── quick_sort.c
    ├── linear_search.c
    └── binary_search.c
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/arkadeepdas29/algorithm-visualizer.git
cd algorithm-visualizer
```

### 2. Create and activate a virtual environment

#### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Compile the C programs

Make sure GCC is installed on your system.

```bash
gcc c_engine/bubble_sort.c -o c_engine/bubble_sort.exe
gcc c_engine/selection_sort.c -o c_engine/selection_sort.exe
gcc c_engine/insertion_sort.c -o c_engine/insertion_sort.exe
gcc c_engine/merge_sort.c -o c_engine/merge_sort.exe
gcc c_engine/quick_sort.c -o c_engine/quick_sort.exe
gcc c_engine/linear_search.c -o c_engine/linear_search.exe
gcc c_engine/binary_search.c -o c_engine/binary_search.exe
```

### 5. Start the Flask backend

```bash
python backend/app.py
```

The backend runs locally at:

```text
http://127.0.0.1:5000
```

### 6. Run the frontend

Open [frontend/index.html](frontend/index.html) in a browser, or use a local development server such as VS Code Live Server.

## Usage

### Sorting Algorithms

1. Enter an array such as `64, 25, 12, 22, 11`.
2. Select a sorting algorithm.
3. Choose the animation speed.
4. Click the Start button.
5. Watch the algorithm execute step by step.
6. Review the comparison and operation statistics.

### Searching Algorithms

1. Enter an array such as `64, 25, 12, 22, 11`.
2. Select either Linear Search or Binary Search.
3. Enter the search target value.
4. Choose the animation speed.
5. Click the Start button.
6. Observe the search process and the final result.

> For Binary Search, the array is automatically sorted before the search begins.

## Time Complexity

| Algorithm | Best | Average | Worst |
| --- | --- | --- | --- |
| Bubble Sort | O(n) | O(n²) | O(n²) |
| Selection Sort | O(n²) | O(n²) | O(n²) |
| Insertion Sort | O(n) | O(n²) | O(n²) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) |
| Linear Search | O(1) | O(n) | O(n) |
| Binary Search | O(1) | O(log n) | O(log n) |

## Future Improvements

- Add more sorting algorithms
- Add more searching algorithms
- Add algorithm-specific explanations
- Add step-by-step pseudocode
- Add space complexity information
- Improve visualization controls
- Improve mobile responsiveness
- Add performance comparisons between algorithms

## Author

- Arkadeep Das
- B.Tech in Computer Science & Engineering
- Techno India University

## License

This project is created for educational and learning purposes.

No formal open-source license file is included in the repository at this time, so the project should be treated as educational code for learning and demonstration.

---

For the actual project files, see:

- [frontend/index.html](frontend/index.html)
- [frontend/style.css](frontend/style.css)
- [frontend/script.js](frontend/script.js)
- [backend/app.py](backend/app.py)
- [backend/requirements.txt](backend/requirements.txt)
- [c_engine](c_engine)