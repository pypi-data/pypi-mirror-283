import unittest
import os
import sys
import rasterio
import numpy as np

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from satellite_image_classification.classification import classify_image

class TestClassification(unittest.TestCase):
    def setUp(self):
        self.input_tiff = 'test_input.tiff'
        self.output_tiff = 'test_output.tiff'
        self.create_test_tiff(self.input_tiff)

    def tearDown(self):
        os.remove(self.input_tiff)
        os.remove(self.output_tiff)

    def create_test_tiff(self, filename):
        with rasterio.open(filename, 'w', driver='GTiff', height=10, width=10, count=3, dtype='uint8') as dst:
            data = np.random.randint(0, 255, (3, 10, 10), dtype='uint8')
            dst.write(data)

    def test_classify_image(self):
        classify_image(self.input_tiff, self.output_tiff)
        with rasterio.open(self.output_tiff) as src:
            data = src.read(1)
            self.assertEqual(data.shape, (10, 10))

if __name__ == '__main__':
    unittest.main()
