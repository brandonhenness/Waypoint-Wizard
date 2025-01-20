import io
from PIL import Image, ImageDraw, ImageFont
from waypoint_mapper import (
    CubiomesWrapper,
    MinecraftVersion,
    Dimension,
    Flags,
    Colors,
)


class MapGenerator:
    def __init__(self, dll_path: str = "./waypoint_mapper/cubiomes_wrapper.dll"):
        self.cubiomes = CubiomesWrapper(dll_path)

    def generate_map_image(
        self,
        name,
        color,
        x,
        z,
        dimension,
        seed,
        version,
        flags,
        zoom=1.0,
        aspect_ratio=4 / 3,
    ):
        # Calculate the height and width in pixels, ensuring the height is at least 600 pixels
        # height = max(600, int(600 * zoom))
        height = 600
        width = int(height * aspect_ratio)

        # Calculate pix4cell based on the zoom level, ensuring it's at least 1
        if zoom >= 1:
            pix4cell = int(zoom)
            scale = 1
        else:
            pix4cell = 1
            scale = int(1 / zoom)

        # Calculate the size of the image adjusted for the scale and pix4cell
        sx = (width * scale) // pix4cell
        sz = (height * scale) // pix4cell

        # Calculate the center coordinates of the image
        cx = x - (sx // 2)
        cz = z - (sz // 2)

        y = 15  # Near sea level
        sy = 1  # Single vertical layer

        # Generate the biome image
        self.cubiomes.generate_biome_image(
            version.value,
            flags.value,
            seed,
            dimension.value,
            cx,
            cz,
            sx,
            sz,
            y,
            sy,
            pix4cell,
            scale,
        )

        # Retrieve the image data from the DLL
        image_data = self.cubiomes.get_image_buffer()
        image = Image.open(io.BytesIO(image_data))

        # Annotate the image with a triangle and text
        self._annotate_image(image, name, color)

        return image

    def _annotate_image(self, image, name, color):
        draw = ImageDraw.Draw(image)
        center_x = image.width // 2
        center_y = image.height // 2
        triangle_color = color.value
        triangle_size = 20
        outline_thickness = 2
        outline_color = "black"

        # Define the coordinates for the triangle with the point at the bottom
        triangle = [
            (center_x, center_y),
            (center_x - triangle_size, center_y - triangle_size),
            (center_x + triangle_size, center_y - triangle_size),
        ]

        # Draw black outline
        for i in range(-outline_thickness, outline_thickness + 1):
            for j in range(-outline_thickness, outline_thickness + 1):
                offset_triangle = [(x + i, y + j) for x, y in triangle]
                draw.polygon(offset_triangle, fill=outline_color)

        draw.polygon(triangle, fill=triangle_color)

        # Add text above the triangle
        wrapped_text = wrap_text(name, 21)
        text_color = triangle_color
        font_size = 24
        try:
            # font = ImageFont.truetype("./Minecraftia-Regular.ttf", font_size) TODO: Find a font file that works with multiple font sizes.
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        total_text_height = 0
        text_positions = []
        for line in wrapped_text:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_height = text_bbox[3] - text_bbox[1]
            total_text_height += text_height
            text_positions.append((line, text_height))

        text_y = center_y - triangle_size - total_text_height - 10

        current_y = text_y
        for line, text_height in text_positions:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = center_x - text_width // 2
            for i in range(-outline_thickness, outline_thickness + 1):
                for j in range(-outline_thickness, outline_thickness + 1):
                    draw.text(
                        (text_x + i, current_y + j), line, font=font, fill=outline_color
                    )
            draw.text((text_x, current_y), line, fill=text_color, font=font)
            current_y += text_height


# Text wrapping function
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
