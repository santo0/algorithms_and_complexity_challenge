import unittest
import random
from preprocessing import call_get_median

class PreprocTesting(unittest.TestCase):
    def test_get_median(self):
        for _ in range(1, 100):
            samples_list = [('', '', random.randint(0, i))
                            for i in range(random.randint(1, 500))]
            self.assertEqual(call_get_median(samples_list),
                             sorted(samples_list)[len(samples_list) // 2])


if __name__ == '__main__':
    unittest.main()
