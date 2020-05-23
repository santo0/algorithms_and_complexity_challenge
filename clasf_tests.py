'''
    Title: clasf_tests.py
    Author: Guillem Camats Felip, Adria Juve Sanchez, Marti La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
import unittest
from classify import create_clustering


class ClasfTesting(unittest.TestCase):
    '''Unit test of classify module'''
    def test_clasf_1(self):
        '''Test of cluster creating'''
        score_matrix = [[1, 2, 3, 4],
                        [2, 1, 3, 4],
                        [3, 3, 1, 4],
                        [4, 4, 4, 1]]
        final_clusters = create_clustering([2, 3], score_matrix)
        self.assertEqual(final_clusters, {0: [0, 1, 2], 3: [3]})


if __name__ == '__main__':
    unittest.main()
