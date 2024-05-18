#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void) {
  string message = get_string("Message: ");

  for (int i = 0, n = strlen(message); i < n; i++) {
    int ascii = message[i];
    int bits[BITS_IN_BYTE];

    for (int j = BITS_IN_BYTE - 1; j >= 0; j--) {
      bits[j] = ascii % 2;
      ascii /= 2;
    }

    for (int j = 0; j < BITS_IN_BYTE; j++) {
      print_bulb(bits[j]);
    }
    printf("\n");
  }
}

void print_bulb(int bit) {
  if (bit == 0) {
    printf("\U000026AB"); // Black circle emoji
  } else if (bit == 1) {
    printf("\U0001F7E1"); // Yellow circle emoji
  }
}
