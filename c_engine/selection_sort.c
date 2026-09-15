#include <stdio.h>

#define MAX_ARRAY_SIZE 1000

void selectionSort(
    int array[],
    int size,
    unsigned long long *comparisons,
    unsigned long long *swaps
) {
    for (int currentIndex = 0; currentIndex < size - 1; currentIndex++) {
        int minimumIndex = currentIndex;

        for (int index = currentIndex + 1; index < size; index++) {
            (*comparisons)++;

            printf(
                "STEP:COMPARE:%d:%d\n",
                minimumIndex,
                index
            );

            if (array[index] < array[minimumIndex]) {
                minimumIndex = index;
            }
        }

        if (minimumIndex != currentIndex) {
            int temporaryValue = array[currentIndex];
            array[currentIndex] = array[minimumIndex];
            array[minimumIndex] = temporaryValue;

            (*swaps)++;

            printf(
                "STEP:SWAP:%d:%d\n",
                currentIndex,
                minimumIndex
            );
        }
    }
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

    selectionSort(
        array,
        numberOfElements,
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