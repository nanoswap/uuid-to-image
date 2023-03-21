import uuid
import numpy as np
import imageio
import math

uuid = uuid.uuid4()
print(uuid)

width, height = 100, 100
image = np.zeros((width, height, 3), dtype=np.uint8)

def update_pixel(x, y, r, g, b, image):
    image[x, y, :] = (0xFF * r, 0xF * g, 0xFF * b)
    return image

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

uuid_str = str(uuid).replace('-', '')

last = 0
for a, b, c in zip(uuid_str, uuid_str[1:], uuid_str[2:]):

    red = int(a, 16) / 16
    green = int(b, 16) / 16
    blue = int(c, 16) / 16

    x_loc = int(red+green * width)
    y_loc = int(green+blue * height)
    size = int((red + green + blue) * 16)
    last += x_loc / (last + 1)

    for x in range(x_loc - size, x_loc + size):
        for y in range(y_loc - size, y_loc + size):
            if x < width and y < height and x > 0 and y > 0:
                if distance(x_loc, y_loc, x, y) < size or a > b:
                    if int(a, 16) / (int(b, 16) + 1) > int(c, 16):
                        image = update_pixel(x, y, red - green*width, green, blue, image)
                    elif int(c, 16) / (int(a, 16) + 1) < int(b, 16):
                        image = update_pixel(x, y, green, red - blue*height, blue, image)
                    else:
                        image = update_pixel(x, y, red - blue*height, blue - red*height, green * red*width, image)

imageio.imwrite('output.png', image)
