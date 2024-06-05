#include <stdint.h>

int main(void)
{
    float a = 3.14159 / 2.71828;
    float b = 2.71828;
    uint16_t c = 65450;

    while (b == c) {
        a = b - a;
    }

    return 0;
}