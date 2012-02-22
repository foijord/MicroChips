#include "utils.h"
#include <stdio.h>
#include <assert.h>

void 
utils_read_array(const char * filename, int * array)
{
  int index = 0;
  char line[64];

  FILE * file = fopen(filename, "rt");
  assert(file && "file not found!");

  while (fgets(line, 64, file)) {
    array[index++] = atoi(line);
  }
  fclose(file);
}

