import unittest
import random
from preprocessing import MedianSample, call_get_median, get_samples_of_median_length_by_country, get_fasta_sequences
class PreprocTesting(unittest.TestCase):
    def test_get_median(self):
        for _ in range(1, 100):
            samples_list = [ ('','',random.randint(0,i)) for i in range(random.randint(1, 500))]
            self.assertEqual(call_get_median(samples_list), sorted(samples_list)[len(samples_list) // 2])


if __name__ == '__main__':
    unittest.main()
