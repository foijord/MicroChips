
#ifndef POKERLIB_H
#define POKERLIB_H

#ifdef __cplusplus
extern "C" {
#endif

void compute_pre_flop_equity_vs_random(int cards[2], int counts[3]);
void compute_pre_flop_equity_vs_1_hand(int cards[4], int counts[3]);
void rank_all_7_card_hands(void);

#ifdef __cplusplus
}
#endif
	
#endif /* POKERLIB_H */
