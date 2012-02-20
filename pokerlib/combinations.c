#include <stdio.h>

int combinations(int * c, int n, int k)
{
  int j = k - 1;

  if (c[j] < n - 1) {
    c[j] += 1;
    return 1;
  }
    
  while (j >= 0 && c[j] == n - k + j) 
    j--;

  if (j < 0) return 0;

  c[j]++;

  for (j += 1; j < k; j++)
    c[j] = c[j-1] + 1;

  return 1;
}

void printc(int * c)
{
  printf("{ %i %i %i }\n", c[0], c[1], c[2]);
}

int main(int argc, char ** argv) 
{
  int c[3] = { 0, 1, 1 };
  while (combinations(c, 5, 3)) {
    printc(c);
  }
}
