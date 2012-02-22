
#ifndef COMBINATIONS_H
#define COMBINATIONS_H

#ifdef __cplusplus
extern "C" {
#endif

int * first_combination(int k);
int next_combination(int * c, const int n, const int k);

#ifdef __cplusplus
}
#endif

#endif // COMBINATIONS_H
