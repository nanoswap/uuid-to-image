# UUID to Image Generator

## Usage

```python
import uuid
import imageio
from uuidtoimage.generate import Generate
uuid = uuid.uuid4()
width, height = 100, 100

image = Generate.generate_image(width, height, uuid)
imageio.imwrite('output.png', image)
```

::: uuidtoimage.generate.Generate
    handler: python
    options:
      members:
        - generate_image
        - distance
        - update_pixel
      show_root_heading: true
      show_source: true
