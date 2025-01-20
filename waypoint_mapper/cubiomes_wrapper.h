#ifndef CUBIOMES_WRAPPER_H
#define CUBIOMES_WRAPPER_H

#include <stdint.h>

void generate_biome_image(int version, uint32_t flags, uint64_t seed, int dimension, int x, int z, int sx, int sz, int y, int sy, int pix4cell, int scale);
unsigned char *get_image_buffer();
int get_image_size();

#endif
