#include <cs50.h>
#include <stdio.h>

int main(void) {
  long card_number = get_long("Number: ");
  long temp = card_number;
  int sum = 0;
  int digit_count = 0;
  int last_two_digits = 0;

  while (temp > 0) {
    int digit = temp % 10;

    if (digit_count % 2 == 1) {
      digit *= 2;
      if (digit > 9) {
        sum += digit / 10 + digit % 10;
      } else {
        sum += digit;
      }
    } else {
      sum += digit;
    }

    if (digit_count == 0 || digit_count == 1) {
      last_two_digits += digit * (digit_count == 0 ? 1 : 10);
    }

    digit_count++;
    temp /= 10;
  }

  int first_two = last_two_digits;
  while (card_number >= 100) {
    card_number /= 10;
  }
  first_two = card_number;

  if (sum % 10 != 0) {
    printf("INVALID\n");
  } else if ((first_two == 34 || first_two == 37) && digit_count == 15) {
    printf("AMEX\n");
  } else if (first_two >= 51 && first_two <= 55 && digit_count == 16) {
    printf("MASTERCARD\n");
  } else if (first_two / 10 == 4 && (digit_count == 13 || digit_count == 16)) {
    printf("VISA\n");
  } else {
    printf("INVALID\n");
  }
}
