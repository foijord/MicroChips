#include "deck.h"
#include "combinations.h"

#include <stdlib.h>
#include <stdio.h>

void 
deck_init_cards(deck_t * self)
{
  int i;
  self->deck_size = 52;
  for (i = 0; i < self->deck_size; i++) self->cards[i] = i;
}

void 
deck_init_with_dead_cards(deck_t * self, int dead_cards[], int num_dead_cards)
{
  int ok, i, j, k = 0;
  self->deck_size = 52 - num_dead_cards;

  for (i = 0; i < self->deck_size; i++) {
    do {
      ok = 1;
      for (j = 0; j < num_dead_cards; j++) {
        if (dead_cards[j] == k) { ok = 0; k++; }
      }
    } while (!ok);
    self->cards[i] = k++;
  }
}

void
deck_init_deal(deck_t * self, const int deal_count)
{
  int i;
  for (i = 0; i < deal_count - 1; i++) self->board[i] = i;
  self->board[deal_count - 1] = deal_count - 2;
  self->deal_count = deal_count;
}

int
deck_deal_next(deck_t * self)
{
  return next_combination(self->board, self->deck_size, self->deal_count);
}
