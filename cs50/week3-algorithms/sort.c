#include <cs50.h>
#include <stdio.h>

void swap(int *a, int *b);

int main(void) {
  int arr[] = {64, 34, 25, 12, 22, 11, 90};
  int n = 7;

  printf("Original array: ");
  for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
  }
  printf("\n");

  // Bubble Sort
  for (int i = 0; i < n - 1; i++) {
    bool swapped = false;
    for (int j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        swap(&arr[j], &arr[j + 1]);
        swapped = true;
      }
    }
    if (!swapped) {
      break;
    }
  }

  printf("Sorted array: ");
  for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
  }
  printf("\n");

  return 0;
}

void swap(int *a, int *b) {
  int temp = *a;
  *a = *b;
  *b = temp;
}
