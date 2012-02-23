
#ifndef EVALUATORS_H
#define EVALUATORS_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct eval7 eval7_t;

eval7_t * eval7_get(void);
void eval7_exit(void);
void eval7_reset_deck(eval7_t * self);
int eval7_deal_card(eval7_t * self, int card);
int eval7_get_rank(eval7_t * self, int c1, int c2, int c3, int c4, int c5, int c6, int c7);

#ifdef __cplusplus
}
#endif

#endif // EVALUATORS_H
