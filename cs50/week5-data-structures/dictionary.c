#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HASH_SIZE 26

typedef struct node {
  char word[46];
  struct node *next;
} node;

node *table[HASH_SIZE];
unsigned int word_count = 0;

unsigned int hash(const char *word) { return toupper(word[0]) - 'A'; }

bool load(const char *dictionary) {
  FILE *file = fopen(dictionary, "r");
  if (file == NULL) {
    return false;
  }

  char word[46];
  while (fscanf(file, "%s", word) != EOF) {
    node *n = malloc(sizeof(node));
    if (n == NULL) {
      return false;
    }

    strcpy(n->word, word);
    unsigned int index = hash(word);
    n->next = table[index];
    table[index] = n;
    word_count++;
  }

  fclose(file);
  return true;
}

bool check(const char *word) {
  char lower[46];
  for (int i = 0, n = strlen(word); i <= n; i++) {
    lower[i] = tolower(word[i]);
  }

  unsigned int index = hash(lower);
  for (node *ptr = table[index]; ptr != NULL; ptr = ptr->next) {
    if (strcmp(lower, ptr->word) == 0) {
      return true;
    }
  }
  return false;
}

unsigned int size(void) { return word_count; }

bool unload(void) {
  for (int i = 0; i < HASH_SIZE; i++) {
    node *ptr = table[i];
    while (ptr != NULL) {
      node *tmp = ptr;
      ptr = ptr->next;
      free(tmp);
    }
  }
  return true;
}

// large test
