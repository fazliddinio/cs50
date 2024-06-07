#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct node {
  int number;
  struct node *next;
} node;

int main(int argc, char *argv[]) {
  node *list = NULL;

  for (int i = 1; i < argc; i++) {
    int number = atoi(argv[i]);

    node *n = malloc(sizeof(node));
    if (n == NULL) {
      return 1;
    }
    n->number = number;
    n->next = NULL;

    // Insert at beginning
    n->next = list;
    list = n;
  }

  // Print the list
  printf("List: ");
  for (node *ptr = list; ptr != NULL; ptr = ptr->next) {
    printf("%i ", ptr->number);
  }
  printf("\n");

  // Free memory
  while (list != NULL) {
    node *tmp = list->next;
    free(list);
    list = tmp;
  }

  return 0;
}

// pointers study
