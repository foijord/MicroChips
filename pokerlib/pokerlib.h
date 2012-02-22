
#ifndef POKERLIB_H
#define POKERLIB_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct eval7 eval7_t;

eval7_t * eval7_get(void);
void eval7_exit(void);
int eval7_deal_card(eval7_t * self, const char * card);
int eval7_get_rank(eval7_t * self, int c1, int c2, int c3, int c4, int c5, int c6, int c7);

#ifdef __cplusplus
}
#endif
	
#endif /* POKERLIB_H */