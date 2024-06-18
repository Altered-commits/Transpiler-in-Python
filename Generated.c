#include <stdio.h>
#include <math.h>
#include <stdint.h>

int main(void)
{
    float b = 0.0;
    float a = 0.0;
    double c = 0.0;

    scanf("%f%f", &a, &b);

    c = cos(a) + sin(b);

    printf("cos + sin of a and b is: %lf", c);

    float d = 0.0;

    scanf("%f", &d);
    printf("Factorial of d is: %lf", tgamma(d+1));

    return 0;
}