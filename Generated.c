#include <math.h>
#include <stdio.h>
#include <stdint.h>

uint8_t myAddUCUC(uint8_t a, uint8_t b)
{
    printf("A: %hhu, B: %hhu", a, b);
    return a + b;
}

uint8_t myFuncUCUC(uint8_t a, uint8_t b)
{
    uint8_t c = myAddUCUC(a, b);
    return c;
}

int main(void)
{
    int8_t a = (10 + 20) / 30 * 40 % 97;
    int8_t b = 10 - 0;
    uint8_t c = (a != b) && ((b >= a) || (b <= a)) && (a == b);

    printf("Variable c Evaluated: %hhu, %lf\n", c, tgamma(100.0+1));

    if (c) {
        printf("C Valid\n");
    }
    else if (!(c)) {
        printf("C Not Valid\n");
    }
    else {
        printf("No opinion\n");
    }

    while (b > 0) {
        printf("B: %hhd\n", b);
        b = b - 1;
    }

    for (uint8_t i = 0; i < 10; i = i + 1) {
        printf("I: %hhu\n", i);
    }

    do {
        printf("A: %hhu\n", a);
        a = a - 1;
    }
    while (a > 1);

    printf("MyFunc: %hhu", myFuncUCUC(10, 20));
    puts("EEEEEEEEEEEE");

    return 0;
}