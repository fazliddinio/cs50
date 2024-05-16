#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void) {
  string message = get_string("Message: ");
  // TODO: convert to binary
}

void print_bulb(int bit) {
  if (bit == 0) printf("0");
  else printf("1");
}
