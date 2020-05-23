import unittest
import random
from classify import clustering, create_clustering
class ClasfTesting(unittest.TestCase):  
    def test_clasf_1(self):
        score_matrix = [[1,2,3,4],
                        [2,1,3,4],
                        [3,3,1,4],
                        [4,4,4,1]]
        final_clusters = create_clustering([2,3],score_matrix)
        self.assertEqual(final_clusters, {0: [0, 1, 2], 3: [3]})
 
if __name__ == '__main__':
    unittest.main()
