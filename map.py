import ctypes
from ctypes import c_int, c_uint64, POINTER, c_ubyte, string_at
from PIL import Image, ImageDraw, ImageFont
import io

# Load the DLL
cubiomes = ctypes.CDLL("./waypoint_mapper/cubiomes_wrapper.dll")

# Define the function signatures
cubiomes.generate_biome_image.argtypes = [
    c_int,
    c_int,
    c_uint64,
    c_int,
    c_int,
    c_int,
    c_int,
    c_int,
    c_int,
    c_int,
    c_int,
]
cubiomes.generate_biome_image.restype = None
cubiomes.get_image_buffer.argtypes = []
cubiomes.get_image_buffer.restype = POINTER(c_ubyte)
cubiomes.get_image_size.argtypes = []
cubiomes.get_image_size.restype = c_int

zoom = 0
# Define the parameters
version = 25  # Example version, adjust as necessary
flags = 0  # Example flags, adjust as necessary
seed = 132389425772377
dimension = 0  # Example dimension (e.g., overworld)
x = -(39272 // 16) - 32
z = -(21656 // 16) - 32
sx = 64  # Width in chunks
sz = 64  # Height in chunks
y = 15  # Near sea level
sy = 1  # Single vertical layer
pix4cell = 0  # Resolution of the output image

# Call the function to generate the biome image
cubiomes.generate_biome_image(
    version, flags, seed, dimension, x, z, sx, sz, y, sy, pix4cell
)

# Retrieve the image data from the DLL
image_size = cubiomes.get_image_size()
image_buffer = cubiomes.get_image_buffer()

# Convert the image data to a format Pillow can read
image_data = string_at(image_buffer, image_size)
image = Image.open(io.BytesIO(image_data))


def wrap_text(text, line_length):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            if current_line:
                lines.append(current_line)
            if len(word) > line_length:
                while len(word) > line_length:
                    lines.append(word[: line_length - 1] + "-")
                    word = word[line_length - 1 :]
                current_line = word
            else:
                current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# Draw a triangle pointing down at the center of the image
draw = ImageDraw.Draw(image)
center_x = image.width // 2
center_y = image.height // 2
triangle_color = "aqua"
triangle_size = 10  # Size of the triangle
outline_thickness = 2  # Outline thickness
outline_color = "black"

# Define the coordinates for the triangle with the point at the bottom
triangle = [
    (center_x, center_y + triangle_size),  # Bottom point
    (center_x - triangle_size, center_y - triangle_size // 2),  # Top left point
    (center_x + triangle_size, center_y - triangle_size // 2),  # Top right point
]

# Draw black outline
for i in range(-outline_thickness, outline_thickness + 1):
    for j in range(-outline_thickness, outline_thickness + 1):
        offset_triangle = [(x + i, y + j) for x, y in triangle]
        draw.polygon(offset_triangle, fill=outline_color)

draw.polygon(triangle, fill=triangle_color)

# Add text above the triangle
text = "This is a multiline text example"
wrapped_text = wrap_text(text, 21)
text_color = "aqua"
font_size = 28
try:
    font = ImageFont.truetype("./Minecraftia-Regular.ttf", font_size)
except IOError:
    font = ImageFont.load_default()

# Get the size of the text
total_text_height = 0
text_positions = []
for line in wrapped_text:
    text_bbox = draw.textbbox((0, 0), line, font=font)
    text_height = text_bbox[3] - text_bbox[1]
    total_text_height += text_height
    text_positions.append((line, text_height))

text_y = center_y - triangle_size - total_text_height - 5

current_y = text_y
for line, text_height in text_positions:
    text_bbox = draw.textbbox((0, 0), line, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = center_x - text_width // 2
    # Draw text outline
    for i in range(-outline_thickness, outline_thickness + 1):
        for j in range(-outline_thickness, outline_thickness + 1):
            draw.text((text_x + i, current_y + j), line, font=font, fill=outline_color)
    draw.text((text_x, current_y), line, fill=text_color, font=font)
    current_y += text_height

# Save the final image
png_filename = "output_image.png"
image.save(png_filename)

print(f"Converted PPM image to {png_filename} with a triangle and text at the center.")
