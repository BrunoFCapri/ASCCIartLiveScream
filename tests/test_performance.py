import unittest
from src.utils.performance import monitor_performance

class TestPerformance(unittest.TestCase):

    def test_monitor_performance(self):
        # Simulate a performance monitoring scenario
        fps, processing_time = monitor_performance()
        
        # Check if FPS is within a reasonable range
        self.assertGreater(fps, 0, "FPS should be greater than 0")
        self.assertLess(fps, 60, "FPS should be less than 60")
        
        # Check if processing time is reasonable
        self.assertGreater(processing_time, 0, "Processing time should be greater than 0")

if __name__ == '__main__':
    unittest.main()