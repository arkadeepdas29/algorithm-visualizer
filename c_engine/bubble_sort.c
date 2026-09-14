#include <stdio.h>

#define MAX_ARRAY_SIZE 1000

/* Print every element in an array on one line. */
void printArray(const int array[], int size) {
    for (int index = 0; index < size; index++) {
        printf("%d", array[index]);

        if (index < size - 1) {
            printf(" ");
        }
    }

    printf("\n");
}

/*
 * Sort an array in ascending order using Bubble Sort.
 * The pointer parameters allow this function to update both counters for main.
 */
void bubbleSort(int array[], int size, unsigned long long *comparisons, unsigned long long *swaps) {
    for (int end = size - 1; end > 0; end--) {
        int swappedInThisPass = 0;

        for (int index = 0; index < end; index++) {
            (*comparisons)++;

            if (array[index] > array[index + 1]) {
                int temporaryValue = array[index];
                array[index] = array[index + 1];
                array[index + 1] = temporaryValue;

                (*swaps)++;
                swappedInThisPass = 1;
            }
        }

        /* If a whole pass made no swaps, the array is already sorted. */
        if (!swappedInThisPass) {
            break;
        }
    }
}

int main(void) {
    int array[MAX_ARRAY_SIZE];
    int numberOfElements;
    unsigned long long comparisons = 0;
    unsigned long long swaps = 0;

    printf("Enter number of elements: ");
    if (scanf("%d", &numberOfElements) != 1) {
        printf("Invalid input. Please enter a whole number.\n");
        return 1;
    }

    if (numberOfElements < 1 || numberOfElements > MAX_ARRAY_SIZE) {
        printf("Please enter a number from 1 to %d.\n", MAX_ARRAY_SIZE);
        return 1;
    }

    printf("Enter elements:\n");
    for (int index = 0; index < numberOfElements; index++) {
        if (scanf("%d", &array[index]) != 1) {
            printf("Invalid element input. Please enter whole numbers only.\n");
            return 1;
        }
    }

    printf("\nOriginal array:\n");
    printArray(array, numberOfElements);

    bubbleSort(array, numberOfElements, &comparisons, &swaps);

    printf("\nSorted array:\n");
    printArray(array, numberOfElements);
    printf("\nComparisons: %llu\n", comparisons);
    printf("Swaps: %llu\n", swaps);

    return 0;
}
