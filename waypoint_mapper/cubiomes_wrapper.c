#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "../cubiomes/generator.h"
#include "../cubiomes/util.h"
#include "../cubiomes/biomenoise.h"
#include "../cubiomes/tables/btree18.h"
#include "../cubiomes/tables/btree192.h"
#include "../cubiomes/tables/btree19.h"
#include "../cubiomes/tables/btree20.h"

static unsigned char *image_buffer = NULL;
static int image_size = 0;

void generate_biome_image(int version, uint32_t flags, uint64_t seed, int dimension,
                          int x, int z, int sx, int sz, int y, int sy, int pix4cell, int scale)
{
    Generator g;
    setupGenerator(&g, version, flags);
    applySeed(&g, dimension, seed);

    Range r;
    r.scale = scale;
    r.x = x, r.z = z;
    r.sx = sx, r.sz = sz;
    r.y = y, r.sy = sy;

    int *biomeIds = allocCache(&g, r);
    genBiomes(&g, biomeIds, r);

    int imgWidth = pix4cell * r.sx, imgHeight = pix4cell * r.sz;
    unsigned char biomeColors[256][3];
    initBiomeColors(biomeColors);
    image_size = 3 * imgWidth * imgHeight + 15 + snprintf(NULL, 0, "P6\n%d %d\n255\n", imgWidth, imgHeight);
    image_buffer = (unsigned char *)malloc(image_size);
    int header_len = sprintf((char *)image_buffer, "P6\n%d %d\n255\n", imgWidth, imgHeight);
    biomesToImage(image_buffer + header_len, biomeColors, biomeIds, r.sx, r.sz, pix4cell, 2);

    free(biomeIds);
}

unsigned char *get_image_buffer()
{
    return image_buffer;
}

int get_image_size()
{
    return image_size;
}
