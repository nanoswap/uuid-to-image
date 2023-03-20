import uuid
import numpy as np
import imageio

uuid = uuid.uuid4()
print(uuid)

width, height = 100, 100
image = np.zeros((width, height, 3), dtype=np.uint8)

def update_pixel(x, y, r, g, b, image):
    image[x, y, :] = (0xFF * r, 0xF * g, 0xFF * b)
    return image

for x in range(25, 75):
    for y in range(25, 75):
        image = update_pixel(x, y, y/x, x/y, (x+y)/2, image)

imageio.imwrite('output.png', image)
