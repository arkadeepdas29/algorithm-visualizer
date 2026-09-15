#include <stdio.h>

#define MAX_ARRAY_SIZE 1000

void insertionSort(
    int array[],
    int size,
    unsigned long long *comparisons,
    unsigned long long *swaps
) {
    for (int currentIndex = 1; currentIndex < size; currentIndex++) {
        int key = array[currentIndex];
        int index = currentIndex - 1;

        while (index >= 0) {
            (*comparisons)++;

            printf(
                "STEP:COMPARE:%d:%d\n",
                index,
                index + 1
            );

            if (array[index] > key) {
                array[index + 1] = array[index];

                (*swaps)++;

                printf(
                    "STEP:SWAP:%d:%d\n",
                    index,
                    index + 1
                );

                index--;
            } else {
                break;
            }
        }

        array[index + 1] = key;
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

    insertionSort(
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