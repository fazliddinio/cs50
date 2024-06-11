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

// TODO: load, check, size, unload

// load implemented

// check working

// all functions done
