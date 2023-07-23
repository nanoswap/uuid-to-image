import uuid
import numpy as np
import imageio
import math

def update_pixel(x, y, r, g, b, image):
    # Adjusted to handle RGBA
    r = int(0xFF * r)
    g = int(0xFF * g)
    b = int(0xFF * b)
    a = image[x, y, 3]  # Preserve alpha
    image[x, y, :] = ((r, g, b, a) + image[x, y, :]) // 2
    return image

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

def generate_image(width, height, uuid):
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

        for x in range(x_loc - size, x_loc + size):
            for y in range(y_loc - size, y_loc + size):
                if x < width and y < height and x >= 0 and y >= 0:
                    if distance(center[0], center[1], x, y) < radius:
                        if int(a, 16) / (int(b, 16) + 1) > int(c, 16):
                            image = update_pixel(x, y, red - green*width, green, blue, image)
                        elif int(c, 16) / (int(a, 16) + 1) < int(b, 16):
                            image = update_pixel(x, y, green, red - blue*height, blue, image)
                        else:
                            image = update_pixel(x, y, red - blue*height, blue - red*height, green * red*width, image)
                    else:
                        angle = math.atan2(y - center[1], x - center[0])
                        new_x = int(center[0] + radius * math.cos(angle))
                        new_y = int(center[1] + radius * math.sin(angle))

                        if int(a, 16) / (int(b, 16) + 1) > int(c, 16):
                            image = update_pixel(new_x, new_y, red - green*width, green, blue, image)
                        elif int(c, 16) / (int(a, 16) + 1) < int(b, 16):
                            image = update_pixel(new_x, new_y, green, red - blue*height, blue, image)
                        else:
                            image = update_pixel(new_x, new_y, red - blue*height, blue - red*height, green * red*width, image)

    # Set alpha channel to 255 for all pixels inside the circle, else 0
    for x in range(width):
        for y in range(height):
            if distance(center[0], center[1], x, y) < radius:
                image[y, x, 3] = 255
            else:
                image[y, x, 3] = 0

    return image

if __name__ == "__main__":
    for i in range(8):
        cur_uuid = uuid.uuid4()
        print(cur_uuid)

        width, height = 100, 100
        image = generate_image(width, height, cur_uuid)
        imageio.imwrite(f'images/output_{cur_uuid}.png', image)
        imageio.imwrite(f'last_output.png', image)
