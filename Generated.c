#include <stdint.h>

int main(void)
{
    float a = 3.14159 / 2.71828;
    float b = 2.71828;
    uint16_t c = 65450;

    if (a == b) {
        c = c + 1;
    }
    else if (b == c) {
        c = c + 2;
    }
    else {
        c = c + 3;
    }

    return 0;
}