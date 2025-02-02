#include <stdint.h>
#include <stdio.h>

//Global vars
uint8_t _i = 0;
uint8_t _r = 10;
uint8_t _s = 1;

void _My_loop()
{
    for (uint8_t i = _i; i < _r; i = i + _s) {
        printf("Index: %hhu", i);
    }
}

int main(void)
{
    _My_loop();

    return 0;
}