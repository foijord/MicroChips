
#include "evaluators.h"

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "utils.h"
#include "constants.h"

struct eval7 {
  int * deck;
  int * ranks;
  int * flushes;
  int * flush_check;
} eval7;

void
eval7_init(eval7_t * self)
{
  self->ranks = (int*) malloc(size_7_card_ranks);
  self->flushes = (int*) malloc(size_7_card_flushes);
  self->flush_check = (int*) malloc(size_7_card_flush_check);

  utils_read_array("../data/ranks_7.dat", self->ranks);
  utils_read_array("../data/flushes_7.dat", self->flushes);
  utils_read_array("../data/flushcheck_7.dat", self->flush_check);

  self->deck = (int *)malloc(size_52_card_deck);
  int i;
  for (i = 0; i < 52; i++) {
    self->deck[i] = (rank_keys7[i >> 2] << flush_bit_shift) + suit_keys7[i & 3];
  }
}

void
eval7_exit(void)
{
  eval7_t * self = eval7_get();
  free(self->deck);
  free(self->ranks);
  free(self->flushes);
  free(self->flush_check);
}

eval7_t *
eval7_get(void)
{
  static eval7_t * self = NULL;
  if (!self) {
    self = (eval7_t *)malloc(sizeof(eval7));
    eval7_init(self);
  }
  return self;
}

int 
eval7_get_rank(eval7_t * self, int c1, int c2, int c3, int c4, int c5, int c6, int c7)
{
  unsigned int key = self->deck[c1] +
                     self->deck[c2] +
                     self->deck[c3] +
                     self->deck[c4] +
                     self->deck[c5] +
                     self->deck[c6] +
                     self->deck[c7];

  int flush_suit = self->flush_check[key & flush_bit_mask];
      
  if (flush_suit < 0) {
    return self->ranks[key >> flush_bit_shift];
  }

  key = 0;
  if (suit_keys7[c1 & 3] == flush_suit) key += flush_keys[c1 >> 2];
  if (suit_keys7[c2 & 3] == flush_suit) key += flush_keys[c2 >> 2];
  if (suit_keys7[c3 & 3] == flush_suit) key += flush_keys[c3 >> 2];
  if (suit_keys7[c4 & 3] == flush_suit) key += flush_keys[c4 >> 2];
  if (suit_keys7[c5 & 3] == flush_suit) key += flush_keys[c5 >> 2];
  if (suit_keys7[c6 & 3] == flush_suit) key += flush_keys[c6 >> 2];
  if (suit_keys7[c7 & 3] == flush_suit) key += flush_keys[c7 >> 2];

  // assert here that flushes[key] != 0 ?
  return self->flushes[key];
}

