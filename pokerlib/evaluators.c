
#include "evaluators.h"

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "utils.h"
#include "constants.h"

struct eval7 {
  int deck[52];
  int * ranks;
  int * flushes;
  int * flush_check;
} eval7;

void
eval7_init(eval7_t * self)
{
  int i;
  self->ranks = (int*) malloc(size_7_card_ranks);
  self->flushes = (int*) malloc(size_7_card_flushes);
  self->flush_check = (int*) malloc(size_7_card_flush_check);

  utils_read_array("../data/ranks_7.dat", self->ranks);
  utils_read_array("../data/flushes_7.dat", self->flushes);
  utils_read_array("../data/flushcheck_7.dat", self->flush_check);

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

static int get_flush_rank(eval7_t * self, int c1, int c2, int c3, int c4, int c5, int c6, int c7, int flush_suit)
{
	unsigned int key = 0;

	if (suit_keys7[c1 & 3] == flush_suit) key += flush_keys[c1 >> 2];
	if (suit_keys7[c2 & 3] == flush_suit) key += flush_keys[c2 >> 2];
	if (suit_keys7[c3 & 3] == flush_suit) key += flush_keys[c3 >> 2];
	if (suit_keys7[c4 & 3] == flush_suit) key += flush_keys[c4 >> 2];
	if (suit_keys7[c5 & 3] == flush_suit) key += flush_keys[c5 >> 2];
	if (suit_keys7[c6 & 3] == flush_suit) key += flush_keys[c6 >> 2];
	if (suit_keys7[c7 & 3] == flush_suit) key += flush_keys[c7 >> 2];

	return self->flushes[key];	
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
  return (flush_suit < 0) ? self->ranks[key >> flush_bit_shift] : get_flush_rank(self, c1, c2, c3, c4, c5, c6, c7, flush_suit);
}

void
eval7_rank_hands(eval7_t * self, int h1, int h2, int h3, int h4, int b1, int b2, int b3, int b4, int b5, int counts[3])
{
  unsigned int key = self->deck[b1] +
                     self->deck[b2] +
                     self->deck[b3] +
                     self->deck[b4] +
                     self->deck[b5];

  unsigned int key1 = key + self->deck[h1] + self->deck[h2];
  unsigned int key2 = key + self->deck[h3] + self->deck[h4];

  int flush_suit1 = self->flush_check[key1 & flush_bit_mask];
  int flush_suit2 = self->flush_check[key2 & flush_bit_mask];

	int rank1 = (flush_suit1 < 0) ? self->ranks[key1 >> flush_bit_shift] : get_flush_rank(self, h1, h2, b1, b2, b3, b4, b5, flush_suit1);
	int rank2 = (flush_suit2 < 0) ? self->ranks[key2 >> flush_bit_shift] : get_flush_rank(self, h3, h4, b1, b2, b3, b4, b5, flush_suit2);

	if (rank1 > rank2) counts[0]++;
	if (rank1 < rank2) counts[1]++;
	if (rank1 == rank2) counts[2]++;
}
