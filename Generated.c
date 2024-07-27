#include <stdio.h>
#include <stdint.h>

void do_printC(int8_t a)
{
    printf("Inside function loop: %hhd + %hhd\n", a, (a + 1));
}

void my_functionCF(int8_t a, float b)
{
    for (int8_t i = a; i < b; i = i + 1) {
        do_printC(i);
    }
}

void do_printF(float a)
{
    printf("Inside function loop: %f + %f\n", a, (a + 1));
}

void my_functionFF(float a, float b)
{
    for (float i = a; i < b; i = i + 1) {
        do_printF(i);
    }
}

int main(void)
{
    uint8_t c = 10;
    int8_t a = c - 1 - 8;
    float b = 0.0;

    scanf("%hhd%f", &a, &b);

    my_functionCF(a, b);
    my_functionFF(1.5, 10.5);

    return 0;
}