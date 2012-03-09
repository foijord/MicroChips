#include "combinations.h"

int
next_combination(int c[], const int n, const int k)
{
  int j = k - 1;
  if (c[j] < n - 1) {
    c[j] += 1;
    return 1;
  }
  while (j >= 0 && c[j] == n - k + j) j--;
  if (j < 0) return 0;
  c[j]++;
  for (j += 1; j < k; j++) c[j] = c[j-1] + 1;
  return 1;
}

int
deal_next(int deck[48], int board[5])
{
  int j = 4;
  if (board[j] < 47) {
    board[j]++;
    return 1;
  }
  while (j >= 0 && board[j] == 43 + j) j--;
  if (j < 0) return 0;
  board[j]++;
  for (j++; j < 5; j++) board[j] = board[j-1] + 1;
  return 1;
}
