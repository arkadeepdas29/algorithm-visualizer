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
void bubbleSort(
    int array[],
    int size,
    unsigned long long *comparisons,
    unsigned long long *swaps
) {
    for (int end = size - 1; end > 0; end--) {
        int swappedInThisPass = 0;

        for (int index = 0; index < end; index++) {
            (*comparisons)++;

            /* Report every comparison. */
            printf("STEP:COMPARE:%d:%d\n", index, index + 1);

            if (array[index] > array[index + 1]) {
                int temporaryValue = array[index];
                array[index] = array[index + 1];
                array[index + 1] = temporaryValue;

                (*swaps)++;
                swappedInThisPass = 1;

                /* Report every swap. */
                printf("STEP:SWAP:%d:%d\n", index, index + 1);
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

    /* Read number of elements from stdin. */
    if (scanf("%d", &numberOfElements) != 1) {
        fprintf(stderr, "Invalid input.\n");
        return 1;
    }

    if (numberOfElements < 1 || numberOfElements > MAX_ARRAY_SIZE) {
        fprintf(
            stderr,
            "Number of elements must be between 1 and %d.\n",
            MAX_ARRAY_SIZE
        );
        return 1;
    }

    /* Read array elements from stdin. */
    for (int index = 0; index < numberOfElements; index++) {
        if (scanf("%d", &array[index]) != 1) {
            fprintf(stderr, "Invalid element input.\n");
            return 1;
        }
    }

    /* Sort the array using Bubble Sort. */
    bubbleSort(array, numberOfElements, &comparisons, &swaps);

    /*
     * Machine-readable output for Python.
     */
    printf("SORTED:");
    for (int index = 0; index < numberOfElements; index++) {
        printf(" %d", array[index]);
    }
    printf("\n");

    printf("COMPARISONS: %llu\n", comparisons);
    printf("SWAPS: %llu\n", swaps);

    return 0;
}