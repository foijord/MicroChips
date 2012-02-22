#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

#include "utils.h"
#include "constants.h"
#include "pokerlib.h"
#include "combinations.h"

struct eval7 {
  int * deck;
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

  self->deck = (int *)malloc(size_52_card_deck);

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
eval7_deal_card(eval7_t * self, const char * card)
{
  return 0;
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

  return self->flushes[key];
}

void
calculate_pre_flop_equity()
{
  int rank1, rank2;
  int wins1 = 0;
  int wins2 = 0;
  int draws = 0;
  int count = 0;
  
  eval7_t * e7 = eval7_get();

  int As = eval7_deal_card(e7, "As");
  int Ah = eval7_deal_card(e7, "Ah");

  int Ks = eval7_deal_card(e7, "Ks");
  int Kh = eval7_deal_card(e7, "Kh");

  int * c = first_combination(5);
  while (next_combination(c, 48, 5)) {
    rank1 = eval7_get_rank(e7, As, Ah, c[0], c[1], c[2], c[3], c[4]);
    rank2 = eval7_get_rank(e7, Ks, Kh, c[0], c[1], c[2], c[3], c[4]);
    if (rank1 > rank2) wins1++;
    if (rank1 < rank2) wins2++;
    if (rank1 == rank2) draws++;
  }

  printf("wins0: %i, wins2: %i, draws: %i\n", wins1, wins2, draws);
}

void
test_deck()
{
  // assemble a deck of card symbols
  int i;
  int max_card_index = 51;

  char ** deck = (char**)malloc(52 * sizeof(char*));
  for (i = 0; i < 52; i++) {
    deck[i] = (char*) malloc(2);
    sprintf(deck[i], "%s%s", rank_symbols[i >> 2], suit_symbols[i & 3]);
  }

  // deal As
  for (i = 0; i < max_card_index; i++) {
    if (strcmp(deck[i], "As") == 0) {
      // swap
      char * tmp = deck[max_card_index];
      deck[max_card_index] = deck[i];
      deck[i] = tmp;
      max_card_index--;
      break;
    }
  }
  // deal Jc
  for (i = 0; i < max_card_index; i++) {
    if (strcmp(deck[i], "Jc") == 0) {
      // swap
      char * tmp = deck[max_card_index];
      deck[max_card_index] = deck[i];
      deck[i] = tmp;
      max_card_index--;
      break;
    }
  }

  for (i = 0; i < 52; i++) {
    printf("deck[%i]: %s\n", i, deck[i]);
  }
}

void 
compute_all_7_card_hands()
{
  int count = 0;
  // make sure rank computation is not optimized away by making it volatile
  volatile int rank;
  clock_t tic, tac;

  eval7_t * e7 = eval7_get();
  int * c = first_combination(7);

  tic = clock();

  while (next_combination(c, 52, 7)) {
    rank = eval7_get_rank(e7, c[0], c[1], c[2], c[3], c[4], c[5], c[6]);
    count++;
  }
  
  tac = clock();
  printf("Ranked %i 7-card poker hands in %f seconds\n", count, (double)(tac - tic) / CLOCKS_PER_SEC);

  eval7_exit();
}

int 
main(int argc, char ** argv) 
{
  test_deck();  
  return 1;
}
