#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[]) {
  if (argc != 2) {
    printf("Usage: ./caesar key\n");
    return 1;
  }
  // TODO: validate key and encrypt
  return 0;
}

// validate argv[1] is numeric
