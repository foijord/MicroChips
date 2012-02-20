#include <stdio.h>

int comb(int * c, int n, int k)
{
  int j = k - 1;

  if (c[j] < n - 1) {
    c[j] += 1;
    return 1;
  }
    
  while ((j >= 0) && (c[j] >= n - k + j))
    j--;

  if (j < 0) return 0;

  c[j]++;

  for (j += 1; j < k; j++)
    c[j] = c[j-1] + 1;

  return 1;
}

void printc(int * c)
{
  printf("{ %i %i %i %i %i }\n", c[0], c[1], c[2], c[3], c[4]);
}

int main(int argc, char ** argv) 
{
  int c[5] = { 0, 1, 2, 3, 4 };
  //printc(c);
  while (comb(c, 52, 5)) {
    //printc(c);
  }
}
