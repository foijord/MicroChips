
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

void deck_init(deck_t * self, int deal_count, int dead_cards[], int num_dead_cards);
int deck_deal(deck_t * self);

#ifdef __cplusplus
}
#endif

#endif // DECK_H
