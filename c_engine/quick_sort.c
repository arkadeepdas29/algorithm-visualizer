#include <stdio.h>

#define MAX_ARRAY_SIZE 1000

int partition(
    int array[],
    int low,
    int high,
    unsigned long long *comparisons,
    unsigned long long *swaps
) {
    int pivot = array[high];
    int smallerIndex = low - 1;

    for (int currentIndex = low; currentIndex < high; currentIndex++) {
        (*comparisons)++;

        printf(
            "STEP:COMPARE:%d:%d\n",
            currentIndex,
            high
        );

        if (array[currentIndex] < pivot) {
            smallerIndex++;

            if (smallerIndex != currentIndex) {
                int temporaryValue = array[smallerIndex];
                array[smallerIndex] = array[currentIndex];
                array[currentIndex] = temporaryValue;

                (*swaps)++;

                printf(
                    "STEP:SWAP:%d:%d\n",
                    smallerIndex,
                    currentIndex
                );
            }
        }
    }

    if (smallerIndex + 1 != high) {
        int temporaryValue = array[smallerIndex + 1];
        array[smallerIndex + 1] = array[high];
        array[high] = temporaryValue;

        (*swaps)++;

        printf(
            "STEP:SWAP:%d:%d\n",
            smallerIndex + 1,
            high
        );
    }

    return smallerIndex + 1;
}

void quickSort(
    int array[],
    int low,
    int high,
    unsigned long long *comparisons,
    unsigned long long *swaps
) {
    if (low >= high) {
        return;
    }

    int pivotIndex = partition(
        array,
        low,
        high,
        comparisons,
        swaps
    );

    quickSort(
        array,
        low,
        pivotIndex - 1,
        comparisons,
        swaps
    );

    quickSort(
        array,
        pivotIndex + 1,
        high,
        comparisons,
        swaps
    );
}

int main(void) {
    int array[MAX_ARRAY_SIZE];
    int numberOfElements;

    unsigned long long comparisons = 0;
    unsigned long long swaps = 0;

    if (scanf("%d", &numberOfElements) != 1) {
        fprintf(stderr, "Invalid input.\n");
        return 1;
    }

    if (
        numberOfElements < 1 ||
        numberOfElements > MAX_ARRAY_SIZE
    ) {
        fprintf(
            stderr,
            "Number of elements must be between 1 and %d.\n",
            MAX_ARRAY_SIZE
        );
        return 1;
    }

    for (int index = 0; index < numberOfElements; index++) {
        if (scanf("%d", &array[index]) != 1) {
            fprintf(stderr, "Invalid element input.\n");
            return 1;
        }
    }

    quickSort(
        array,
        0,
        numberOfElements - 1,
        &comparisons,
        &swaps
    );

    printf("SORTED:");

    for (int index = 0; index < numberOfElements; index++) {
        printf(" %d", array[index]);
    }

    printf("\n");

    printf("COMPARISONS: %llu\n", comparisons);
    printf("SWAPS: %llu\n", swaps);

    return 0;
}