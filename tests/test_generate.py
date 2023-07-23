import unittest
import uuid

import numpy as np
from uuidtoimage.generate import Generate

class TestImageGeneration(unittest.TestCase):
    def test_update_pixel(self):
        image = np.zeros((100, 100, 4), dtype=np.uint8)

        # Test with an image of zeroes
        new_image = Generate.update_pixel(50, 50, 0.6, 0.3, 0.1, image)
        self.assertEqual(new_image[50, 50, 0], 76)  # 0xFF * 0.6 = 153, but then divided by 2 because of averaging with 0
        self.assertEqual(new_image[50, 50, 1], 38)  # 0xFF * 0.3 = 76, but then divided by 2 because of averaging with 0
        self.assertEqual(new_image[50, 50, 2], 12)  # 0xFF * 0.1 = 25, but then divided by 2 because of averaging with 0
        self.assertEqual(new_image[50, 50, 3], 0)

        # Test with an image of ones (converted to appropriate scale)
        image = np.ones((100, 100, 4), dtype=np.uint8) * 255
        new_image = Generate.update_pixel(50, 50, 0.6, 0.3, 0.1, image)
        self.assertEqual(new_image[50, 50, 0], int((153+255)/2))  # averaging 153 and 255
        self.assertEqual(new_image[50, 50, 1], int((76+255)/2))   # averaging 76 and 255
        self.assertEqual(new_image[50, 50, 2], int((25+255)/2))   # averaging 25 and 255
        self.assertEqual(new_image[50, 50, 3], 255)

    def test_distance(self):
        self.assertEqual(Generate.distance(0, 0, 3, 4), 5)
        self.assertEqual(Generate.distance(0, 0, -3, -4), 5)
        self.assertAlmostEqual(Generate.distance(0, 0, 1, 1), 1.41421356, places=7)

    def test_generate_image(self):
        test_uuid = uuid.UUID("00000000-0000-0000-0000-000000000000")
        image = Generate.generate_image(100, 100, test_uuid)
        self.assertEqual(image.shape, (100, 100, 4))

        # Check the generated image is a circle
        center = (50, 50)
        for x in range(100):
            for y in range(100):
                if Generate.distance(center[0], center[1], x, y) < 50:
                    self.assertEqual(image[y, x, 3], 255)
                else:
                    self.assertEqual(image[y, x, 3], 0)
