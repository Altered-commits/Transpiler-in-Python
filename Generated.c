#include <math.h>
#include <stdio.h>
#include <stdint.h>

int main(void)
{
    float b = 0.0;
    float a = 0.0;
    double c = 0.0;

    scanf("%f%f", &a, &b);

    c = cos(a) + sin(b);

    printf("cos + sin of a and b is: %lf", c);

    return 0;
}