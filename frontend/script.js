// The visualizer state is kept in one place so sorting algorithms can use it later.
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
  return Array.from({ length }, () => Math.floor(Math.random() * (max - min + 1)) + min);
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

  elements.arrayStatus.textContent = `${visualizerState.array.length} values ready`;
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

/** Update the statistics display. */
function updateStatistics() {
  elements.comparisons.textContent = visualizerState.comparisons;
  elements.swaps.textContent = visualizerState.swaps;
  elements.timeComplexity.textContent = "O(n²)";
}

/**
 * Pause for an amount of time based on the speed slider.
 * A higher slider value gives a shorter pause and a faster animation.
 */
function sleep() {
  const delayInMilliseconds = 20 + (100 - visualizerState.speed) * 8;
  return new Promise((resolve) => setTimeout(resolve, delayInMilliseconds));
}

/** Change a displayed bar after its matching array value changes. */
function updateBar(index) {
  const bar = getBars()[index];
  const value = visualizerState.array[index];

  bar.style.height = `${value}%`;
  bar.title = `Value: ${value}`;
}

/** Enable or disable controls while an animation is running. */
function setSortingControls(isSorting) {
  elements.startButton.disabled = isSorting;
  elements.algorithmSelect.disabled = isSorting;
  elements.startButton.textContent = isSorting ? "Sorting..." : "Start";
}

/**
 * Reset the array and all statistics to their starting state.
 * Increasing runId tells any active sort to stop after its current pause.
 */
function resetVisualizer() {
  visualizerState.runId += 1;
  visualizerState.isSorting = false;
  visualizerState.array = generateRandomArray();
  visualizerState.comparisons = 0;
  visualizerState.swaps = 0;
  renderArray();
  updateStatistics();
  setSortingControls(false);
}

/** Keep the selected speed ready for a future animation feature. */
function updateSpeed() {
  visualizerState.speed = Number(elements.speedSlider.value);
  elements.speedValue.textContent = `${visualizerState.speed}%`;
}

/** Sort the current array using Bubble Sort and animate every comparison. */
async function bubbleSort() {
  const currentRunId = visualizerState.runId;
  const arrayLength = visualizerState.array.length;

  // Each pass moves the largest remaining value to the end of the array.
  for (let end = arrayLength - 1; end > 0; end -= 1) {
    let swappedInThisPass = false;

    for (let index = 0; index < end; index += 1) {
      if (currentRunId !== visualizerState.runId) return;

      const bars = getBars();
      bars[index].classList.add("comparing");
      bars[index + 1].classList.add("comparing");
      visualizerState.comparisons += 1;
      updateStatistics();
      await sleep();

      if (currentRunId !== visualizerState.runId) return;

      if (visualizerState.array[index] > visualizerState.array[index + 1]) {
        [visualizerState.array[index], visualizerState.array[index + 1]] = [
          visualizerState.array[index + 1],
          visualizerState.array[index],
        ];
        visualizerState.swaps += 1;
        updateBar(index);
        updateBar(index + 1);
        bars[index].classList.replace("comparing", "swapping");
        bars[index + 1].classList.replace("comparing", "swapping");
        updateStatistics();
        swappedInThisPass = true;
        await sleep();
      }

      if (currentRunId !== visualizerState.runId) return;
      clearBarHighlights();
    }

    // If a complete pass made no swaps, the array is already sorted.
    if (!swappedInThisPass) break;
  }

  if (currentRunId === visualizerState.runId) {
    clearBarHighlights();
    getBars().forEach((bar) => bar.classList.add("sorted"));
    elements.arrayStatus.textContent = "Array sorted";
  }
}

/** Start Bubble Sort and make sure only one animation can run at a time. */
async function startVisualization() {
  if (visualizerState.isSorting || elements.algorithmSelect.value !== "bubble") return;

  const currentRunId = visualizerState.runId;
  visualizerState.isSorting = true;
  setSortingControls(true);

  try {
    await bubbleSort();
  } finally {
    // A reset starts a newer run, so an older sort must not change its controls.
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
