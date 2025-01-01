#include <stdio.h>
#include <math.h>
#include <stdint.h>

int main(void)
{
    uint8_t a = (10 + 20) / 30 * 40 % 97;
    uint8_t b = 10;
    uint8_t c = (a != b) && ((b >= a) || (b <= a)) && (a == b);

    printf("Variable c Evaluated: %hhu, %lf", c, tgamma(100.0+1));

    return 0;
}