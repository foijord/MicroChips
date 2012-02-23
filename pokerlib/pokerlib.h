
#ifndef POKERLIB_H
#define POKERLIB_H

#ifdef __cplusplus
extern "C" {
#endif

void compute_pre_flop_equity_vs_random(int c0, int c1, int counts[3]);
void compute_pre_flop_equity_vs_1_hand(int c0, int c1, int c2, int c3, int counts[3]);
void rank_all_7_card_hands(void);

#ifdef __cplusplus
}
#endif
	
#endif /* POKERLIB_H */
