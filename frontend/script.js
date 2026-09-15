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
 * Pause for an amount of time based on the speed slider.
 * A higher slider value gives a shorter pause.
 */
function sleep() {
    const delayInMilliseconds = 20 + (100 - visualizerState.speed) * 8;

    return new Promise((resolve) => {
        setTimeout(resolve, delayInMilliseconds);
    });
}

/** Change a displayed bar after its matching array value changes. */
function updateBar(index) {
    const bar = getBars()[index];
    const value = visualizerState.array[index];

    if (!bar) return;

    bar.style.height = `${value}%`;
    bar.title = `Value: ${value}`;
}

/** Enable or disable controls while an operation is running. */
function setSortingControls(isSorting) {
    elements.startButton.disabled = isSorting;
    elements.algorithmSelect.disabled = isSorting;

    elements.startButton.textContent = isSorting
        ? "Sorting..."
        : "Start";
}

/** Reset the array and all statistics. */
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
    elements.speedValue.textContent = `${visualizerState.speed}%`;
}

/**
 * Send the current array to Flask.
 * Flask then runs the C Bubble Sort executable.
 */
async function runBubbleSortOnBackend(array) {
    const response = await fetch("http://127.0.0.1:5000/api/bubble-sort", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            array: array,
        }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Backend request failed.");
    }

    return data;
}

/**
 * Animate the transition from the current array
 * to the sorted array returned by the C backend.
 */
async function animateBackendResult(originalArray, result) {
    const currentRunId = visualizerState.runId;
    const sortedArray = result.sorted_array;

    visualizerState.comparisons = result.comparisons;
    visualizerState.swaps = result.swaps;

    updateStatistics();

    // Show the original array before starting the animation.
    visualizerState.array = [...originalArray];
    renderArray();
    updateStatistics();

    // Move values toward their final positions one by one.
    for (let index = 0; index < sortedArray.length; index += 1) {
        if (currentRunId !== visualizerState.runId) return;

        const targetValue = sortedArray[index];
        const currentIndex = visualizerState.array.indexOf(
            targetValue,
            index
        );

        if (currentIndex === -1) continue;

        if (currentIndex !== index) {
            const bars = getBars();

            bars[index]?.classList.add("comparing");
            bars[currentIndex]?.classList.add("comparing");

            await sleep();

            if (currentRunId !== visualizerState.runId) return;

            [
                visualizerState.array[index],
                visualizerState.array[currentIndex],
            ] = [
                visualizerState.array[currentIndex],
                visualizerState.array[index],
            ];

            updateBar(index);
            updateBar(currentIndex);

            bars[index]?.classList.replace("comparing", "swapping");
            bars[currentIndex]?.classList.replace("comparing", "swapping");

            await sleep();

            if (currentRunId !== visualizerState.runId) return;

            clearBarHighlights();
        }
    }

    if (currentRunId === visualizerState.runId) {
        visualizerState.array = [...sortedArray];

        renderArray();
        updateStatistics();

        getBars().forEach((bar) => {
            bar.classList.add("sorted");
        });

        elements.arrayStatus.textContent = "Array sorted by C Bubble Sort";
    }
}

/** Start Bubble Sort using the Flask + C backend. */
async function startVisualization() {
    if (
        visualizerState.isSorting ||
        elements.algorithmSelect.value !== "bubble"
    ) {
        return;
    }

    const currentRunId = visualizerState.runId;

    visualizerState.isSorting = true;
    setSortingControls(true);
    clearSortedState();

    const originalArray = [...visualizerState.array];

    try {
        elements.arrayStatus.textContent =
            "Sending array to C Bubble Sort...";

        const result = await runBubbleSortOnBackend(originalArray);

        if (currentRunId !== visualizerState.runId) return;

        await animateBackendResult(originalArray, result);
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
    elements.resetButton.addEventListener("click", resetVisualizer);
    elements.speedSlider.addEventListener("input", updateSpeed);
    elements.startButton.addEventListener("click", startVisualization);

    resetVisualizer();
}

initializeVisualizer();