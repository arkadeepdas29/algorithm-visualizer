#include <stdio.h>

#define MAX_ARRAY_SIZE 1000

void merge(
    int array[],
    int temporaryArray[],
    int left,
    int middle,
    int right,
    unsigned long long *comparisons,
    unsigned long long *writes
) {
    int leftIndex = left;
    int rightIndex = middle + 1;
    int temporaryIndex = left;

    while (leftIndex <= middle && rightIndex <= right) {
        (*comparisons)++;

        printf(
            "STEP:COMPARE:%d:%d\n",
            leftIndex,
            rightIndex
        );

        if (array[leftIndex] <= array[rightIndex]) {
            temporaryArray[temporaryIndex] = array[leftIndex];
            temporaryIndex++;
            leftIndex++;
        } else {
            temporaryArray[temporaryIndex] = array[rightIndex];
            temporaryIndex++;
            rightIndex++;
        }
    }

    while (leftIndex <= middle) {
        temporaryArray[temporaryIndex] = array[leftIndex];
        temporaryIndex++;
        leftIndex++;
    }

    while (rightIndex <= right) {
        temporaryArray[temporaryIndex] = array[rightIndex];
        temporaryIndex++;
        rightIndex++;
    }

    for (int index = left; index <= right; index++) {
        array[index] = temporaryArray[index];

        (*writes)++;

        printf(
            "STEP:WRITE:%d:%d\n",
            index,
            array[index]
        );
    }
}

void mergeSort(
    int array[],
    int temporaryArray[],
    int left,
    int right,
    unsigned long long *comparisons,
    unsigned long long *writes
) {
    if (left >= right) {
        return;
    }

    int middle = left + (right - left) / 2;

    mergeSort(
        array,
        temporaryArray,
        left,
        middle,
        comparisons,
        writes
    );

    mergeSort(
        array,
        temporaryArray,
        middle + 1,
        right,
        comparisons,
        writes
    );

    merge(
        array,
        temporaryArray,
        left,
        middle,
        right,
        comparisons,
        writes
    );
}

int main(void) {
    int array[MAX_ARRAY_SIZE];
    int temporaryArray[MAX_ARRAY_SIZE];
    int numberOfElements;

    unsigned long long comparisons = 0;
    unsigned long long writes = 0;

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

    mergeSort(
        array,
        temporaryArray,
        0,
        numberOfElements - 1,
        &comparisons,
        &writes
    );

    printf("SORTED:");

    for (int index = 0; index < numberOfElements; index++) {
        printf(" %d", array[index]);
    }

    printf("\n");

    printf("COMPARISONS: %llu\n", comparisons);
    printf("WRITES: %llu\n", writes);

    return 0;
}