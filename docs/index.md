# UUID To Image

Convert a uuid to an image in a repeatable way

[github.com/nanoswap/uuid-to-image](https://github.com/nanoswap/uuid-to-image)

# Installation

```
pip install uuidtoimage
```

# Usage

```python
import uuid
import imageio
from uuidtoimage.generate import Generate
uuid = uuid.uuid4()
width, height = 100, 100

image = Generate.generate_image(width, height, uuid)
imageio.imwrite('output.png', image)
```