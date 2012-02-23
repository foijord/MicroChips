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
	while (next_combination(c, 50, 2)) {
		if (c[0] == c0 || c[0] == c1 || c[1] == c0 || c[1] == c1) continue;
		compute_pre_flop_equity_vs_1_hand(c0, c1, c[0], c[1], counts);
	}
}

void
compute_pre_flop_equity_vs_1_hand(int c0, int c1, int c2, int c3, int counts[3])
{
  int rank1, rank2;

  eval7_t * e7 = eval7_get();
  int c[5] = { 0, 1, 2, 3, 3 };

	eval7_reset_deck(e7);
  c0 = eval7_deal_card(e7, c0);
  c1 = eval7_deal_card(e7, c1);
  c2 = eval7_deal_card(e7, c2);
  c3 = eval7_deal_card(e7, c3);

  while (next_combination(c, 48, 5)) {
    rank1 = eval7_get_rank(e7, c0, c1, c[0], c[1], c[2], c[3], c[4]);
    rank2 = eval7_get_rank(e7, c2, c3, c[0], c[1], c[2], c[3], c[4]);
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

void
eval7_test(void)
{
	int rank;
  eval7_t * e7 = eval7_get();
	eval7_deal_card(e7, 49);
	eval7_deal_card(e7, 1);
	eval7_deal_card(e7, 3);
	rank = eval7_get_rank(e7, 0, 4, 8, 12, 16, 50, 51);
	printf("rank: %i\n", rank);
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
	compute_pre_flop_equity_vs_1_hand(0, 4, 1, 5, counts);
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
