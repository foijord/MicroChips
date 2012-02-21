#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static int * deck_keys;
static int * ranks;
static int * flushes;
static int * flush_check;

static int rank_keys5[13] = { 79415, 43258, 19998, 12522, 5624, 2422, 992, 312, 94, 22, 5, 1, 0 };
static int rank_keys6[13] = { 436437, 206930, 90838, 37951, 14270, 5760, 1734, 422, 98, 22, 5, 1, 0 };
static int rank_keys7[13] = { 1479181, 636345, 262349, 83661, 22854, 8698, 2031, 453, 98, 22, 5, 1, 0 };

static int flush_keys[13] = { 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1 };

static int suit_keys6[4] = { 43, 7, 1, 0 };
static int suit_keys7[4] = { 57, 8, 1, 0 };

static int max_5_card_rank_key = 4 * 79415 + 3 * 43258;
static int max_6_card_rank_key = 4 * 436437 + 3 * 206930;
static int max_7_card_rank_key = 4 * 1479181 + 3 * 636345;

static int max_5_card_flush_key = 4096 + 2048 + 1024 + 512 + 256;
static int max_6_card_flush_key = 4096 + 2048 + 1024 + 512 + 256 + 128;
static int max_7_card_flush_key = 4096 + 2048 + 1024 + 512 + 256 + 128 + 64;

static int flush_bit_shift = 9;
static int flush_bit_mask = 511;

void 
read_array(const char * filename, int * array)
{
  FILE * file;
  char line [100];

  file = fopen(filename, "rt");
  if (file == NULL) { 
    perror ("Error opening file");
    return;
  }

  int index = 0;
  while (fgets(line , 100 , file) != NULL) {
    int rank = atoi(line);
    array[index++] = rank;
  }
  fclose(file);
}

void init_seven_eval()
{
  ranks = (int*)malloc((max_7_card_rank_key + 1) * sizeof(int));
  flushes = (int*)malloc((max_7_card_flush_key + 1) * sizeof(int));
  flush_check = (int*)malloc((max_7_card_flush_key + 1) * sizeof(int));
  deck_keys = (int*)malloc(52 * sizeof(int));

  read_array("ranks_7.dat", ranks);
  read_array("flushes_7.dat", flushes);
  read_array("flushcheck_7.dat", flush_check);

  int i;
  for (i = 0; i < 52; i++) { deck_keys[i] = (rank_keys7[i >> 2] << flush_bit_shift) + suit_keys7[i & 3]; }
}

int 
get_rank_of_seven(int c1, int c2, int c3, int c4, int c5, int c6, int c7)
{
  unsigned int key = deck_keys[c1] + 
    deck_keys[c2] + 
    deck_keys[c3] +
    deck_keys[c4] +
    deck_keys[c5] +
    deck_keys[c6] +
    deck_keys[c7];

  int flush_suit = flush_check[key & flush_bit_mask];
      
  if (flush_suit < 0) {
    return ranks[key >> flush_bit_shift];
  }

  key = 0;
  if (suit_keys7[c1 & 3] == flush_suit) key += flush_keys[c1 >> 2];
  if (suit_keys7[c2 & 3] == flush_suit) key += flush_keys[c2 >> 2];
  if (suit_keys7[c3 & 3] == flush_suit) key += flush_keys[c3 >> 2];
  if (suit_keys7[c4 & 3] == flush_suit) key += flush_keys[c4 >> 2];
  if (suit_keys7[c5 & 3] == flush_suit) key += flush_keys[c5 >> 2];
  if (suit_keys7[c6 & 3] == flush_suit) key += flush_keys[c6 >> 2];
  if (suit_keys7[c7 & 3] == flush_suit) key += flush_keys[c7 >> 2];

  return flushes[key];
}

int 
main(int argc, char ** argv) 
{
  init_seven_eval();

  // int * rank_counts = (int*)malloc(7462 * sizeof(int));
  // int i;
  // for (i = 0; i < 7462; i++) {
  //   rank_counts[i] = 0;
  // }

  clock_t tic = clock();

  int count = 0;
  int c1, c2, c3, c4, c5, c6, c7;
  volatile int rank;

  unsigned int key1, key2, key3, key4, key5, key6, key;

  for (c1 = 0; c1 < 46; c1++) {
    key1 = deck_keys[c1];
    for (c2 = c1 + 1; c2 < 47; c2++) {
      key2 = key1 + deck_keys[c2];
      for (c3 = c2 + 1; c3 < 48; c3++) {
        key3 = key2 + deck_keys[c3];
        for (c4 = c3 + 1; c4 < 49; c4++) {
          key4 = key3 + deck_keys[c4];
          for (c5 = c4 + 1; c5 < 50; c5++) {
            key5 = key4 + deck_keys[c5];
            for (c6 = c5 + 1; c6 < 51; c6++) {
              key6 = key5 + deck_keys[c6];
              for (c7 = c6 + 1; c7 < 52; c7++) {
                key = key6 + deck_keys[c7];

                int flush_suit = flush_check[key & flush_bit_mask];
      
                if (flush_suit < 0) {
                  rank = ranks[key >> flush_bit_shift];
                }
                else {
                  key = 0;
                  if (suit_keys7[c1 & 3] == flush_suit) key += flush_keys[c1 >> 2];
                  if (suit_keys7[c2 & 3] == flush_suit) key += flush_keys[c2 >> 2];
                  if (suit_keys7[c3 & 3] == flush_suit) key += flush_keys[c3 >> 2];
                  if (suit_keys7[c4 & 3] == flush_suit) key += flush_keys[c4 >> 2];
                  if (suit_keys7[c5 & 3] == flush_suit) key += flush_keys[c5 >> 2];
                  if (suit_keys7[c6 & 3] == flush_suit) key += flush_keys[c6 >> 2];
                  if (suit_keys7[c7 & 3] == flush_suit) key += flush_keys[c7 >> 2];
                  rank = flushes[key];
                }
              }
            }
          }
        }
      }
    }
  }

  clock_t tac = clock();
  //printf("rank: %i\n", rank);
  printf("Poker hands: %i Elapsed: %f seconds\n", count, (double)(tac - tic) / CLOCKS_PER_SEC);

  // for (i = 7461; i > 7450; i--) {
  //   printf("%i\n", rank_counts[i]);
  // }

  return 1;
}
