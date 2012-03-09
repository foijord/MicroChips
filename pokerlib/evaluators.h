
#ifndef EVALUATORS_H
#define EVALUATORS_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct eval7 eval7_t;

eval7_t * eval7_get(void);
void eval7_exit(void);
int eval7_get_rank(eval7_t * self, int c1, int c2, int c3, int c4, int c5, int c6, int c7);
void eval7_rank_hands(eval7_t * self, int h1, int h2, int h3, int h4, int b1, int b2, int b3, int b4, int b5, int counts[3]);

#ifdef __cplusplus
}
#endif

#endif // EVALUATORS_H
