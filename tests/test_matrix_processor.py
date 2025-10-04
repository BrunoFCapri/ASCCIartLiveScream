import unittest
from src.core.matrix_processor import MatrixProcessor

class TestMatrixProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = MatrixProcessor()

    def test_process_matrix(self):
        input_matrix = [[0, 0, 0], [255, 255, 255]]
        expected_output = ['@', ' ']
        output = self.processor.process_matrix(input_matrix)
        self.assertEqual(output, expected_output)

    def test_process_empty_matrix(self):
        input_matrix = []
        expected_output = []
        output = self.processor.process_matrix(input_matrix)
        self.assertEqual(output, expected_output)

    def test_process_large_matrix(self):
        input_matrix = [[0] * 100 for _ in range(100)]
        output = self.processor.process_matrix(input_matrix)
        self.assertEqual(len(output), 100)

if __name__ == '__main__':
    unittest.main()