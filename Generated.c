#include <stdint.h>

int main(void)
{
    float a = 3.14159 / 2.71828;
    float b = 2.71828;
    float c = 65450;

    while (b == c) {
        while (a == b) {
            if (a == c) {
                a = a - b;
            }
        }
    }

    for (float i = 1; i < 10; i = i + 1.234) {
        c = b * a;
        while (i == 4) {
            b = 0;
            if (b == 0) {
                a = 0;
            }
        }
    }

    return 0;
}