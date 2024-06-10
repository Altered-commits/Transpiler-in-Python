#include <stdint.h>

uint8_t c = 0;
float d = 3.14159 / 2.71828;

uint8_t fibUC(uint8_t x)
{
    if (x == 1) {
        return 1;
    }
    return fibUC(x - 2) + fibUC(x - 1);
}

int main(void)
{
    uint8_t output = fibUC(5);

    return 0;
}