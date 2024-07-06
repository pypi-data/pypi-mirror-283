import unittest
from src.resize_images import resize_image
from PIL import Image
import os

class TestResizeImages(unittest.TestCase):
    def setUp(self):
        # Crée un fichier image de test
        self.test_image_path = 'test_image.jpg'
        self.test_resized_image_path = 'resized_test_image.jpg'
        self.size = (100, 100)
        img = Image.new('RGB', (200, 200), color = 'red')
        img.save(self.test_image_path)

    def test_resize_image(self):
        resize_image(self.test_image_path, self.test_resized_image_path, self.size)
        with Image.open(self.test_resized_image_path) as img:
            self.assertEqual(img.size, self.size)

    def tearDown(self):
        # Supprime les fichiers de test
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.test_resized_image_path):
            os.remove(self.test_resized_image_path)

if __name__ == '__main__':
    unittest.main()
