#include "combinations.h"

#include <stdlib.h>

int *
first_combination(int k)
{
  int i;
  int * combination = (int *)malloc(k * sizeof(int));
  for (i = 0; i < k-1; i++) { combination[i] = i; }
  combination[k-1] = combination[k-2];
  return combination;
}

int
next_combination(int * c, const int n, const int k)
{
  int j = k - 1;
  if (c[j] < n - 1) {
    c[j] += 1;
    return 1;
  }
  while (j >= 0 && c[j] == n - k + j)
    j--;
  if (j < 0)
    return 0;
  c[j]++;
  for (j += 1; j < k; j++)
    c[j] = c[j-1] + 1;
  return 1;
}
