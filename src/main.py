import uuid
import numpy as np
import imageio

uuid = uuid.uuid4()
print(uuid)

width, height = 100, 100
image = np.zeros((width, height, 3), dtype=np.uint8)
image[75, 75, :] = (0xFF, 0xFF, 0xFF)
imageio.imwrite('output.png', image)
