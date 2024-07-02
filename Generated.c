#include <stdio.h>
#include <stdint.h>

void my_functionFF(float a, float b)
{
    for (float i = a; i < b; i = i + 1) {
        printf("Inside function loop: %f\n", i);
    }
}

int main(void)
{
    uint8_t c = 10;
    float a = 0.0 - c - 1;
    float b = 0.0;

    scanf("%f%f", &a, &b);

    my_functionFF(a, b);
    my_functionFF(1.5, 10.5);

    return 0;
}