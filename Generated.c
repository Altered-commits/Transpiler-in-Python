#include <stdio.h>
#include <stdint.h>

int64_t fibonacciUC(uint8_t n)
{
    if (n < 0) {
        printf("Fibonacci cannot be negative");
        return -1;
    }
    if (n == 0 || n == 1) {
        return n;
    }
    return fibonacciUC(n - 1) + fibonacciUC(n - 2);
}

int main(void)
{
    uint8_t a = 0;
    char b[128];

    fgets(b, sizeof(b), stdin);
    printf("Factorial of a is: %d", fibonacciUC(a));

    do {
        uint8_t a = 11;
        a = a + 1;
        printf("%d", a);
    }
    while (a != 20);

    return 0;
}