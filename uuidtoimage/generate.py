import uuid
import numpy as np
import imageio
import math
from typing import Union


class Generate():
    """Generate an image from a UUID.

    This class contains the functions necessary to generate an image
    from a UUID.

    Usage:
    >>> import uuid
    >>> import imageio
    >>> from uuidtoimage.generate import Generate
    >>> uuid = uuid.uuid4()
    >>> width, height = 100, 100
    >>> image = Generate.generate_image(width, height, uuid)
    >>> imageio.imwrite('output.png', image)
    """

    @staticmethod
    def update_pixel(
            x: int,
            y: int,
            r: float,
            g: float,
            b: float,
            image: np.ndarray) -> np.ndarray:
        """Update a pixel in the image using the given RGBA values.

        This function calculates the new RGBA values as an average of
        the existing and the provided values.

        :param x: x coordinate of the pixel
        :param y: y coordinate of the pixel
        :param r: red component
        :param g: green component
        :param b: blue component
        :param image: the image to update
        :return: updated image
        """
        r = int(0xFF * r)
        g = int(0xFF * g)
        b = int(0xFF * b)
        a = image[x, y, 3]  # Preserve alpha
        image[x, y, :] = ((r, g, b, a) + image[x, y, :]) // 2
        return image

    @staticmethod
    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate Euclidean distance between two points.

        :param x1: x coordinate of first point
        :param y1: y coordinate of first point
        :param x2: x coordinate of second point
        :param y2: y coordinate of second point
        :return: distance
        """
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    @staticmethod
    def generate_image(
            width: int,
            height: int,
            uuid: Union[str, uuid.UUID]) -> np.ndarray:
        """Generate an image based on the given width, height, and UUID.

        The UUID is used as a seed to generate a unique image.

        :param width: width of the image
        :param height: height of the image
        :param uuid: a UUID used to seed the image generation
        :return: generated image
        """
        image = np.zeros((width, height, 4), dtype=np.uint8)

        uuid_str = str(uuid).replace('-', '')
        last = 0
        radius = width / 2 if width < height else height / 2
        center = (width // 2, height // 2)

        for a, b, c in zip(uuid_str, uuid_str[1:], uuid_str[2:]):
            red = int(a, 16) / 16
            green = int(b, 16) / 16
            blue = int(c, 16) / 16

            x_loc = int(red + green * width)
            y_loc = int(green + blue * height)
            size = int((red + green + blue) * 16)
            last += x_loc / (last + 1)

            # Iterate over a square around the pixel location
            for x in range(x_loc - size, x_loc + size):
                for y in range(y_loc - size, y_loc + size):
                    if 0 <= x < width and 0 <= y < height:
                        distance = Generate.distance(
                            center[0],
                            center[1],
                            x,
                            y
                        )

                        # If the point is inside the circle, color it,
                        # else move it to the edge and color it
                        if distance < radius:
                            # Color pixel based on the UUID values
                            image = Generate.update_pixel(
                                x,
                                y,
                                red - green * width,
                                green,
                                blue,
                                image
                            )
                        else:
                            # Move the pixel to the edge of the circle
                            # and color it
                            angle = math.atan2(y - center[1], x - center[0])
                            new_x = int(center[0] + radius * math.cos(angle))
                            new_y = int(center[1] + radius * math.sin(angle))
                            image = Generate.update_pixel(
                                new_x,
                                new_y,
                                red - green * width,
                                green,
                                blue,
                                image
                            )

        # Set alpha channel to 255 for all pixels inside the circle, else 0
        for x in range(width):
            for y in range(height):
                if distance(center[0], center[1], x, y) < radius:
                    image[y, x, 3] = 255
                else:
                    image[y, x, 3] = 0

        return image
