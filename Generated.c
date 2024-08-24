#include <stdio.h>
#include <stdint.h>

void do_printUS(uint16_t a)
{
    printf("Inside function loop: %hu + %hu\n", a, (a + 1));
}

void my_functionUSF(uint16_t a, float b)
{
    for (uint16_t i = a; i < b; i = i + 1) {
        do_printUS(i);
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
    uint16_t c = -(-(18000));
    uint16_t a = c - 1 - -8;
    float b = 0.0;

    scanf("%hu%f", &a, &b);

    my_functionUSF(a, b);
    my_functionFF(1.5, 10.5);

    return 0;
}