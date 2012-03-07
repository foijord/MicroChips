#include "pokerlib.h"

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "evaluators.h"
#include "combinations.h"

void
init_deck(int deck[52], int c[], int n)
{
	int ok = 0;
	int i, j, k = 0;

	for (i = 0; i < 52; i++) {
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
compute_pre_flop_equity_vs_random(int c0, int c1, int counts[3])
{
  int c[2] = { 0, 0 };
	int deck[52];
	int hand[2] = { c0, c1 };
	init_deck(deck, hand, 2);

  while (next_combination(c, 50, 2)) {
    compute_pre_flop_equity_vs_1_hand(c0, c1, deck[c[0]], deck[c[1]], counts);
  }
}

void
compute_pre_flop_equity_vs_1_hand(int c0, int c1, int c2, int c3, int counts[3])
{
  int rank1, rank2;
  eval7_t * e7 = eval7_get();
  int c[5] = { 0, 1, 2, 3, 3 };

	int deck[52];
	int hand[4] = { c0, c1, c2, c3 };
	init_deck(deck, hand, 4);
	
  while (next_combination(c, 48, 5)) {
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
  //compute_pre_flop_equity_vs_1_hand(20, 30, 50, 51, counts);
  compute_pre_flop_equity_vs_random(3, 0, counts);
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
