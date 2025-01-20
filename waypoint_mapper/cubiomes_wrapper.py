import ctypes
from ctypes import c_char_p, c_int, c_uint64, c_uint32, POINTER, c_ubyte, string_at
from enum import Enum, IntEnum


class MinecraftVersion(IntEnum):
    MC_UNDEF = 0
    MC_B1_7 = 1
    MC_B1_8 = 2
    MC_1_0 = 3
    MC_1_0_0 = MC_1_0
    MC_1_1 = 4
    MC_1_1_0 = MC_1_1
    MC_1_2 = 5
    MC_1_2_5 = MC_1_2
    MC_1_3 = 6
    MC_1_3_2 = MC_1_3
    MC_1_4 = 7
    MC_1_4_7 = MC_1_4
    MC_1_5 = 8
    MC_1_5_2 = MC_1_5
    MC_1_6 = 9
    MC_1_6_4 = MC_1_6
    MC_1_7 = 10
    MC_1_7_10 = MC_1_7
    MC_1_8 = 11
    MC_1_8_9 = MC_1_8
    MC_1_9 = 12
    MC_1_9_4 = MC_1_9
    MC_1_10 = 13
    MC_1_10_2 = MC_1_10
    MC_1_11 = 14
    MC_1_11_2 = MC_1_11
    MC_1_12 = 15
    MC_1_12_2 = MC_1_12
    MC_1_13 = 16
    MC_1_13_2 = MC_1_13
    MC_1_14 = 17
    MC_1_14_4 = MC_1_14
    MC_1_15 = 18
    MC_1_15_2 = MC_1_15
    MC_1_16_1 = 19
    MC_1_16 = 20
    MC_1_16_5 = MC_1_16
    MC_1_17 = 21
    MC_1_17_1 = MC_1_17
    MC_1_18 = 22
    MC_1_18_2 = MC_1_18
    MC_1_19_2 = 23
    MC_1_19 = 24
    MC_1_19_4 = MC_1_19
    MC_1_20 = 25
    MC_NEWEST = MC_1_20


class Dimension(IntEnum):
    NETHER = -1
    OVERWORLD = 0
    END = 1
    DIM_UNDEF = 1000


class Flags(IntEnum):
    DEFAULT = 0
    LARGE_BIOMES = 1
    NO_BETA_OCEAN = 2
    FORCE_OCEAN_VARIANTS = 4


class Colors(Enum):
    AQUA = "aqua"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    BLACK = "black"
    WHITE = "white"


class CubiomesWrapper:
    def __init__(self, dll_path: str):
        self.cubiomes = ctypes.CDLL(dll_path)
        self._define_function_signatures()

    def _define_function_signatures(self):
        self.cubiomes.generate_biome_image.argtypes = [
            c_int,
            c_uint32,
            c_uint64,
            c_int,
            c_int,
            c_int,
            c_int,
            c_int,
            c_int,
            c_int,
            c_int,
            c_int,
        ]
        self.cubiomes.generate_biome_image.restype = None

        self.cubiomes.get_image_buffer.argtypes = []
        self.cubiomes.get_image_buffer.restype = POINTER(c_ubyte)

        self.cubiomes.get_image_size.argtypes = []
        self.cubiomes.get_image_size.restype = c_int

    def generate_biome_image(
        self, version, flags, seed, dimension, x, z, sx, sz, y, sy, pix4cell, scale
    ):
        self.cubiomes.generate_biome_image(
            version, flags, seed, dimension, x, z, sx, sz, y, sy, pix4cell, scale
        )

    def get_image_buffer(self):
        image_size = self.cubiomes.get_image_size()
        image_buffer = self.cubiomes.get_image_buffer()
        image_data = string_at(image_buffer, image_size)
        return image_data
