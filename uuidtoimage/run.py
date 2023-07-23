import uuid
import imageio
from generate import Generate

if __name__ == "__main__":
    for i in range(8):
        cur_uuid = uuid.uuid4()
        print(cur_uuid)

        width, height = 100, 100
        image = Generate.generate_image(width, height, cur_uuid)
        imageio.imwrite(f'images/output_{cur_uuid}.png', image)
        imageio.imwrite('last_output.png', image)
