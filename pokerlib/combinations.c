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
  int count = 0;
  int c[5] = { 0, 1, 2, 3, 4 };

  /* while (combinations(c, 52, 5)) { */
  /*   count++; */
  /* } */

  for (int c1 = 0; c1 < 48; c1++) {
    for (int c2 = c1 + 1; c2 < 49; c2++) {
      for (int c3 = c2 + 1; c3 < 50; c3++) {
	for (int c4 = c3 + 1; c4 < 51; c4++) {
	  for (int c5 = c4 + 1; c5 < 52; c5++) {
	    count++;
	  }
	}
      }
    }
  }

  printf("count: %i\n", count);
}
