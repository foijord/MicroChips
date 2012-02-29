#include "pokerlib.h"

#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#include "evaluators.h"
#include "combinations.h"

void
compute_pre_flop_equity_vs_random(int c0, int c1, int counts[3])
{
  int c[2] = { 0, 0 };
  while (next_combination(c, 52, 2)) {
    if (c[0] == c0 || c[0] == c1 || c[1] == c0 || c[1] == c1) continue;
    compute_pre_flop_equity_vs_1_hand(c0, c1, c[0], c[1], counts);
  }
}

static int last_deck_index = 51;

void
deal(int * deck, int card)
{
  // swap card with last valid deck index
  int index = last_deck_index;
  int tmp = deck[card];
  deck[card] = deck[last_deck_index];
  deck[last_deck_index] = tmp;
  last_deck_index--;
}

void
compute_pre_flop_equity_vs_1_hand(int c0, int c1, int c2, int c3, int counts[3])
{
  int rank1, rank2;

  eval7_t * e7 = eval7_get();
  int c[5] = { 0, 1, 2, 3, 3 };

  int deck[52] = {  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 
                   13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 
                   26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                   39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51 };

  last_deck_index = 51;
  deal(deck, c0);
  deal(deck, c1);
  deal(deck, c2);
  deal(deck, c3);

  while (next_combination(c, 48, 5)) {
    /* eval7_update_board(e7, deck[c[0]], deck[c[1]], deck[c[2]], deck[c[3]], deck[c[4]]); */
    /* rank1 = eval7_get_rank_with_board(e7, c0, c1); */
    /* rank2 = eval7_get_rank_with_board(e7, c2, c3); */
    
    rank1 = eval7_get_rank(e7, c0, c1, deck[c[0]], deck[c[1]], deck[c[2]], deck[c[3]], deck[c[4]]);
    rank2 = eval7_get_rank(e7, c2, c3, deck[c[0]], deck[c[1]], deck[c[2]], deck[c[3]], deck[c[4]]);
    if (rank1 > rank2) counts[0]++;
    if (rank1 < rank2) counts[1]++;
    if (rank1 == rank2) counts[2]++;
  }
}

void 
rank_all_7_card_hands(void)
{
  int count = 0;
  // make sure rank computation is not optimized away by making it volatile
  volatile int rank;

  eval7_t * e7 = eval7_get();
  int c[7] = { 0, 1, 2, 3, 4, 5, 5 };

  while (next_combination(c, 52, 7)) {
    rank = eval7_get_rank(e7, c[0], c[1], c[2], c[3], c[4], c[5], c[6]);
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
  
  (void)eval7_get(); // initialize here, so we don't time table loading
  
  tic = clock();
  compute_pre_flop_equity_vs_1_hand(0, 1, 4, 5, counts);
  //compute_pre_flop_equity_vs_random(1, 0, counts);
  //rank_all_7_card_hands();
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
