import pytgpt.imager as imager
from typing import List
from typing import Generator
import unittest


class TestImager(unittest.TestCase):

    def setUp(self):
        self.imager = imager.Imager()
        self.prompt: str = "hello world"

    def test_non_stream(self):
        """Test one photo generation"""
        img = self.imager.generate(self.prompt)
        self.assertIsInstance(img, List), "Image not generated"
        self.assertIsInstance(img[0], bytes), "Image not generated"

    def test_stream(self):
        """Test multiple photo generation"""
        generator = self.imager.generate(self.prompt, amount=2, stream=True)
        self.assertIsInstance(generator, Generator)


if __name__ == "__main__":
    unittest.main()
