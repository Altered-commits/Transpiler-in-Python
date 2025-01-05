#include <stdint.h>
#include <math.h>
#include <stdio.h>

//Global vars
uint8_t i = 0;
uint8_t r = 5;
uint8_t ic = 1;

void _My_func()
{
    int32_t __inc = ic + fabs(ceil((-2.13))) + 2;
    for(int i = i; i < r; i = i + __inc)
    {
        printf("%d\n", i);
    }
}

int main(void)
{
    _My_func();

    return 0;
}