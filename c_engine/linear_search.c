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

    for (int i = 0; i < n; i++)
    {
        printf("STEP:COMPARE:%d:%d\n", i, target);

        if (array[i] == target)
        {
            printf("STEP:FOUND:%d:%d\n", i, target);
            printf("FOUND_INDEX: %d\n", i);
            printf("COMPARISONS: %d\n", i + 1);
            return 0;
        }
    }

    printf("STEP:NOT_FOUND:-1:%d\n", target);
    printf("FOUND_INDEX: -1\n");
    printf("COMPARISONS: %d\n", n);

    return 0;
}