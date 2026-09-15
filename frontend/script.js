// The visualizer state is kept in one place.
const visualizerState = {
    array: [],
    comparisons: 0,
    swaps: 0,
    speed: 50,
    isSorting: false,
    runId: 0,
};

const elements = {
    arrayContainer: document.querySelector("#array-container"),
    arrayStatus: document.querySelector("#array-status"),
    comparisons: document.querySelector("#comparisons"),
    swaps: document.querySelector("#swaps"),
    timeComplexity: document.querySelector("#time-complexity"),
    speedSlider: document.querySelector("#speed-slider"),
    speedValue: document.querySelector("#speed-value"),
    resetButton: document.querySelector("#reset-button"),
    startButton: document.querySelector("#start-button"),
    algorithmSelect: document.querySelector("#algorithm-select"),
};

/** Create an array of random whole numbers for the bars. */
function generateRandomArray(length = 30, min = 10, max = 100) {
    return Array.from(
        { length },
        () => Math.floor(Math.random() * (max - min + 1)) + min
    );
}

/** Draw every value in the current array as a vertical bar. */
function renderArray() {
    elements.arrayContainer.innerHTML = "";

    visualizerState.array.forEach((value) => {
        const bar = document.createElement("div");

        bar.className = "array-bar";
        bar.style.height = `${value}%`;
        bar.title = `Value: ${value}`;

        elements.arrayContainer.appendChild(bar);
    });

    elements.arrayStatus.textContent =
        `${visualizerState.array.length} values ready`;
}

/** Return the bars currently displayed in the visualization panel. */
function getBars() {
    return Array.from(elements.arrayContainer.children);
}

/** Remove temporary comparison and swap colors from every bar. */
function clearBarHighlights() {
    getBars().forEach((bar) => {
        bar.classList.remove("comparing", "swapping");
    });
}

/** Remove the final sorted state from every bar. */
function clearSortedState() {
    getBars().forEach((bar) => {
        bar.classList.remove("sorted");
    });
}

/** Update the statistics display. */
function updateStatistics() {
    elements.comparisons.textContent = visualizerState.comparisons;
    elements.swaps.textContent = visualizerState.swaps;
    elements.timeComplexity.textContent = "O(n²)";
}

/**
 * Pause based on the speed slider.
 * Higher speed means a shorter delay.
 */
function sleep() {
    const delayInMilliseconds =
        20 + (100 - visualizerState.speed) * 8;

    return new Promise((resolve) => {
        setTimeout(resolve, delayInMilliseconds);
    });
}

/** Update a displayed bar after its array value changes. */
function updateBar(index) {
    const bar = getBars()[index];

    if (!bar) return;

    const value = visualizerState.array[index];

    bar.style.height = `${value}%`;
    bar.title = `Value: ${value}`;
}

/** Enable or disable controls while sorting. */
function setSortingControls(isSorting) {
    elements.startButton.disabled = isSorting;
    elements.algorithmSelect.disabled = isSorting;

    elements.startButton.textContent =
        isSorting ? "Sorting..." : "Start";
}

/** Reset the array and statistics. */
function resetVisualizer() {
    visualizerState.runId += 1;
    visualizerState.isSorting = false;
    visualizerState.array = generateRandomArray();
    visualizerState.comparisons = 0;
    visualizerState.swaps = 0;

    clearSortedState();
    renderArray();
    updateStatistics();
    setSortingControls(false);
}

/** Update the speed value shown beside the slider. */
function updateSpeed() {
    visualizerState.speed = Number(elements.speedSlider.value);
    elements.speedValue.textContent =
        `${visualizerState.speed}%`;
}

/**
 * Send the current array to Flask.
 * Flask runs the C Bubble Sort executable.
 */
async function runAlgorithmOnBackend(array, algorithm) {
    let endpoint;

    if (algorithm === "bubble") {
        endpoint =
            "http://127.0.0.1:5000/api/bubble-sort";
    } else if (algorithm === "selection") {
        endpoint =
            "http://127.0.0.1:5000/api/selection-sort";
    } else if (algorithm === "insertion") {
        endpoint =
            "http://127.0.0.1:5000/api/insertion-sort";
    } else {
        throw new Error(
            "This algorithm is not implemented yet."
        );
    }

    const response = await fetch(
        endpoint,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                array: array,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.error || "Backend request failed."
        );
    }

    return data;
}

/**
 * Animate the exact comparison and swap steps
 * returned by the C Bubble Sort engine.
 */
async function animateBackendSteps(originalArray, result) {
    const currentRunId = visualizerState.runId;
    const steps = result.steps;

    // Start from the original array.
    visualizerState.array = [...originalArray];
    visualizerState.comparisons = 0;
    visualizerState.swaps = 0;

    renderArray();
    updateStatistics();

    for (const step of steps) {
        if (currentRunId !== visualizerState.runId) {
            return;
        }

        const index1 = step.index1;
        const index2 = step.index2;
        const bars = getBars();

        // Highlight the two elements being compared/swapped.
        bars[index1]?.classList.add("comparing");
        bars[index2]?.classList.add("comparing");

        if (step.type === "compare") {
            visualizerState.comparisons += 1;

            updateStatistics();

            elements.arrayStatus.textContent =
                `Comparing index ${index1} and ${index2}`;

            await sleep();
        }

        if (currentRunId !== visualizerState.runId) {
            return;
        }

        if (step.type === "swap") {
            [
                visualizerState.array[index1],
                visualizerState.array[index2],
            ] = [
                visualizerState.array[index2],
                visualizerState.array[index1],
            ];

            visualizerState.swaps += 1;

            bars[index1]?.classList.replace(
                "comparing",
                "swapping"
            );

            bars[index2]?.classList.replace(
                "comparing",
                "swapping"
            );

            updateBar(index1);
            updateBar(index2);
            updateStatistics();

            elements.arrayStatus.textContent =
                `Swapping index ${index1} and ${index2}`;

            await sleep();
        }

        if (currentRunId !== visualizerState.runId) {
            return;
        }

        clearBarHighlights();
    }

    if (currentRunId === visualizerState.runId) {
        // Use the final result returned by C.
        visualizerState.array = [...result.sorted_array];

        // Use the authoritative totals from C.
        visualizerState.comparisons = result.comparisons;
        visualizerState.swaps = result.swaps;

        renderArray();
        updateStatistics();

        getBars().forEach((bar) => {
            bar.classList.add("sorted");
        });

        elements.arrayStatus.textContent =
            "Array sorted by C Bubble Sort";
    }
}

/** Start Bubble Sort using the Flask + C backend. */
async function startVisualization() {
    const selectedAlgorithm =
        elements.algorithmSelect.value;

    if (visualizerState.isSorting) {
        return;
    }

    if (
        selectedAlgorithm !== "bubble" &&
        selectedAlgorithm !== "selection" &&
        selectedAlgorithm !== "insertion"
    ) {
        elements.arrayStatus.textContent =
            "This algorithm is not implemented yet.";

        return;
    }

    const currentRunId = visualizerState.runId;

    visualizerState.isSorting = true;

    setSortingControls(true);
    clearSortedState();

    const originalArray = [...visualizerState.array];

    try {
        const algorithmName =
            selectedAlgorithm === "bubble"
                ? "Bubble Sort"
                : selectedAlgorithm === "selection"
                  ? "Selection Sort"
                  : "Insertion Sort";

        elements.arrayStatus.textContent =
            `Sending array to C ${algorithmName}...`;

        const result = await runAlgorithmOnBackend(
            originalArray,
            selectedAlgorithm
        );

        if (currentRunId !== visualizerState.runId) {
            return;
        }

        await animateBackendSteps(
            originalArray,
            result
        );
    } catch (error) {
        if (currentRunId === visualizerState.runId) {
            elements.arrayStatus.textContent =
                `Error: ${error.message}`;
        }
    } finally {
        if (currentRunId === visualizerState.runId) {
            visualizerState.isSorting = false;
            setSortingControls(false);
        }
    }
}

function initializeVisualizer() {
    elements.resetButton.addEventListener(
        "click",
        resetVisualizer
    );

    elements.speedSlider.addEventListener(
        "input",
        updateSpeed
    );

    elements.startButton.addEventListener(
        "click",
        startVisualization
    );

    resetVisualizer();
}

initializeVisualizer();