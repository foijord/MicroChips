
#ifndef DECK_H
#define DECK_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct deck deck_t;

struct deck {
  int cards[52];
  int board[7];
  int deck_size;
  int deal_count;
};

void deck_init_cards(deck_t * self);
void deck_init_with_dead_cards(deck_t * self, int dead_cards[], int num_dead_cards);
void deck_init_deal(deck_t * self, const int deal_count);
int deck_deal_next(deck_t * self);

#ifdef __cplusplus
}
#endif

#endif // DECK_H
