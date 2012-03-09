#include "pokerlib.h"

#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#include "evaluators.h"
#include "combinations.h"

void
init_deck(int deck[], int c[], int n)
{
  int ok, i, j, k = 0;
  
  for (i = 0; i < 52 - n; i++) {
    do {
      ok = 1;
      for (j = 0; j < n; j++) {
				if (c[j] == k) { ok = 0; k++; }
      }
    } while (!ok);
    deck[i] = k++;
  }
}

void
compute_pre_flop_equity_vs_random(int cards[2], int counts[3])
{
  int c[2] = { 0, 0 };
  int deck[50];
  init_deck(deck, cards, 2);
  
  while (next_combination(c, 50, 2)) {
    int hand[4] = { cards[0], cards[1], deck[c[0]], deck[c[1]] };
    compute_pre_flop_equity_vs_1_hand(hand, counts);
  }
}

void
compute_pre_flop_equity_vs_1_hand(int cards[4], int counts[3])
{
  int rank1, rank2;
  eval7_t * e7 = eval7_get();
  int c[5] = { 0, 1, 2, 3, 3 };
  
  int deck[48];
  init_deck(deck, cards, 4);
  
  while (deal_next(deck, c)) {
		eval7_rank_hands(e7, cards[0], cards[1], cards[2], cards[3], deck[c[0]], deck[c[1]], deck[c[2]], deck[c[3]], deck[c[4]], counts);
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
  int hand[2] = { 0, 1 };
  
  (void)eval7_get(); // initialize here, so we don't time table loading

  tic = clock();
  compute_pre_flop_equity_vs_random(hand, counts);
	//compute_pre_flop_equity_vs_1_hand(hand, counts);
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
