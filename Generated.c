#include <stdint.h>

uint8_t c = 0;
float d = 1.2252;

int8_t helperFuncUCUC(uint8_t a, uint8_t b)
{
    return a * b - c;
}

int8_t innerFuncUCUC(uint8_t a, uint8_t b)
{
    int8_t result = helperFuncUCUC(a, b);
    if (result > 0) {
        return 1;
    }
    else if (result < 0) {
        return -1;
    }
    else {
        return -10;
    }
}

float outerFuncUCUC(uint8_t x, uint8_t y)
{
    int8_t z = innerFuncUCUC(x, y);
    if (z == 1) {
        return 1;
    }
    else if (z == -1) {
        return -1;
    }
    else {
        return -0.142;
    }
}

int main(void)
{
    float output = outerFuncUCUC(5, 3);

    return 0;
}