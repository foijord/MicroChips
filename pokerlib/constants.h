
#ifndef CONSTANTS_H
#define CONSTANTS_H

const char * rank_symbols[13] = { "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2" };
const char * suit_symbols[4] = { "s", "h", "c", "d" };

const int rank_keys5[13] = { 79415, 43258, 19998, 12522, 5624, 2422, 992, 312, 94, 22, 5, 1, 0 };
const int rank_keys6[13] = { 436437, 206930, 90838, 37951, 14270, 5760, 1734, 422, 98, 22, 5, 1, 0 };
const int rank_keys7[13] = { 1479181, 636345, 262349, 83661, 22854, 8698, 2031, 453, 98, 22, 5, 1, 0 };

const int flush_keys[13] = { 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1 };

const int suit_keys6[4] = { 43, 7, 1, 0 };
const int suit_keys7[4] = { 57, 8, 1, 0 };

const int size_5_card_ranks = (4 * 79415 + 3 * 43258 + 1) * sizeof(int);
const int size_6_card_ranks = (4 * 436437 + 3 * 206930 + 1) * sizeof(int);
const int size_7_card_ranks = (4 * 1479181 + 3 * 636345 + 1) * sizeof(int);

const int size_5_card_flushes = (4096 + 2048 + 1024 + 512 + 256 + 1) * sizeof(int);
const int size_6_card_flushes = (4096 + 2048 + 1024 + 512 + 256 + 128 + 1) * sizeof(int);
const int size_7_card_flushes = (4096 + 2048 + 1024 + 512 + 256 + 128 + 64 + 1) * sizeof(int);

const int size_6_card_flush_check = (6 * 43 + 1) * sizeof(int);
const int size_7_card_flush_check = (7 * 57 + 1) * sizeof(int);

const int size_52_card_deck = 52 * sizeof(int);

const int flush_bit_shift = 9;
const int flush_bit_mask = 511;


#endif CONSTANTS_H
