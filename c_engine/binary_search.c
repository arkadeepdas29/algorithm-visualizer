#include <stdio.h>

int main(void)
{
    int n;
    int target;
    int array[1000];

    scanf("%d", &n);

    if (n < 1 || n > 1000)
    {
        printf("ERROR: Invalid array size\n");
        return 1;
    }

    for (int i = 0; i < n; i++)
    {
        scanf("%d", &array[i]);
    }

    scanf("%d", &target);

    int low = 0;
    int high = n - 1;
    int comparisons = 0;

    while (low <= high)
    {
        int middle = low + (high - low) / 2;

        printf(
            "STEP:COMPARE:%d:%d\n",
            middle,
            target
        );

        comparisons++;

        if (array[middle] == target)
        {
            printf(
                "STEP:FOUND:%d:%d\n",
                middle,
                target
            );

            printf(
                "FOUND_INDEX: %d\n",
                middle
            );

            printf(
                "COMPARISONS: %d\n",
                comparisons
            );

            return 0;
        }

        if (array[middle] < target)
        {
            printf(
                "STEP:RIGHT:%d:%d\n",
                middle,
                target
            );

            low = middle + 1;
        }
        else
        {
            printf(
                "STEP:LEFT:%d:%d\n",
                middle,
                target
            );

            high = middle - 1;
        }
    }

    printf(
        "STEP:NOT_FOUND:-1:%d\n",
        target
    );

    printf("FOUND_INDEX: -1\n");

    printf(
        "COMPARISONS: %d\n",
        comparisons
    );

    return 0;
}