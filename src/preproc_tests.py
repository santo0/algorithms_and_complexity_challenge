'''
    Title: preproc_tests.py
    Author: Guillem Camats Felip, Adria Juve Sanchez, Marti La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
import unittest
import random
from preprocessing import call_get_median

class PreprocTesting(unittest.TestCase):
    '''Unit Test of preprocessing module'''
    def test_get_median(self):
        '''Test of median obtainer'''
        for _ in range(1, 100):
            samples_list = [('', '', random.randint(0, i))
                            for i in range(random.randint(1, 500))]
            self.assertEqual(call_get_median(samples_list),
                             sorted(samples_list)[len(samples_list) // 2])


if __name__ == '__main__':
    unittest.main()
