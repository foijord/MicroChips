#include "pokerlib.h"

#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#include "deck.h"
#include "evaluators.h"

void
compute_pre_flop_equity_vs_random(int cards[2], int counts[3])
{
  deck_t deck;
  deck_init_with_dead_cards(&deck, cards, 2);
  deck_init_deal(&deck, 2);

  while (deck_deal_next(&deck)) {
    int hand[4] = { cards[0], cards[1], deck.cards[deck.board[0]], deck.cards[deck.board[1]] };
    compute_pre_flop_equity_vs_1_hand(hand, counts);
  }
}

void
compute_pre_flop_equity_vs_1_hand(int cards[4], int counts[3])
{
  eval7_t * e7 = eval7_get();

  deck_t deck;
  deck_init_with_dead_cards(&deck, cards, 4);
  deck_init_deal(&deck, 5);

  while (deck_deal_next(&deck)) {
    eval7_rank_hands(e7, cards[0], cards[1], cards[2], cards[3], 
                     deck.cards[deck.board[0]],
                     deck.cards[deck.board[1]],
                     deck.cards[deck.board[2]],
                     deck.cards[deck.board[3]],
                     deck.cards[deck.board[4]],
                     counts);
  }
}

void 
rank_all_7_card_hands(void)
{
  volatile int rank, count = 0;
  eval7_t * e7 = eval7_get();
  deck_t deck;
  deck_init_cards(&deck);
  deck_init_deal(&deck, 7);

  while (deck_deal_next(&deck)) {
    rank = eval7_get_rank(e7, 
                          deck.board[0],
                          deck.board[1],
                          deck.board[2],
                          deck.board[3],
                          deck.board[4],
                          deck.board[5],
                          deck.board[6]);
    count++;
  }
  printf("Ranked %i poker hands.\n", count);
}

int 
main(int argc, char ** argv) 
{
  float seconds;
  clock_t tic, tac;
  int counts[3] = { 0, 0, 0 };
  int sum;
  float p0, p1, p2;
  int hand[4] = { 4, 5, 6, 7 };
  
  (void)eval7_get(); // initialize here, so we don't time table loading

  tic = clock();
  rank_all_7_card_hands();
  /* compute_pre_flop_equity_vs_random(hand, counts); */
  /* compute_pre_flop_equity_vs_1_hand(hand, counts); */
  tac = clock();
  
  sum = counts[0] + counts[1] + counts[2];
  p0 = (float) counts[0] / sum;
  p1 = (float) counts[1] / sum;
  p2 = (float) counts[2] / sum;
  printf("%i %i %i %f %f %f\n", counts[0], counts[1], counts[2], p0, p1, p2);
  
  
  seconds = (float)(tac - tic) / CLOCKS_PER_SEC;
  printf("computation time: %f seconds.\n", seconds);
  
  eval7_exit();
  return 1;
}
