import unittest
from preprocessing import MedianSample
from sequence_alignment import get_samples_alignment_matrix

seq_1 = 'ATTAAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC'
seq_2 = 'ATTAAAGGTTTATACCTTCCAACAAACCAACCAAATCTCTTGTAGATCTCTAAACGAACATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC'
seq_3 = 'TTCGATCTACTTGTAGATCTAGTTCTCTAAACGAACTTTAAAATCTGTGTGGAAAACTGTCACTCGGCTGCATGCTTAGTGCAACGTACGTNACT'
sample_1 = MedianSample('SANTA', '12/25/XX', 'North Pole', sequence=seq_1)
sample_2 = MedianSample('SATAN', '6/6/6', 'Helvetti', sequence=seq_2)
sample_3 = MedianSample('SANTANA', '4/20/20', 'Mexico', sequence=seq_3)

class SeqAlignTesting(unittest.TestCase):  
    def test_seq_align_1(self):
        global sample_1
        global sample_2
        one_to_two = sample_1.align_sequence(sample_2)
        two_to_one = sample_2.align_sequence(sample_1)
        self.assertEqual(one_to_two, two_to_one)
        self.assertEqual(one_to_two, 22)

    def test_seq_align_2(self):
        global sample_1
        global sample_3
        one_to_three = sample_1.align_sequence(sample_3)
        three_to_one = sample_3.align_sequence(sample_1)
        self.assertEqual(one_to_three, three_to_one)
        self.assertEqual(one_to_three, 60)

    def test_seq_align_3(self):
        global sample_2
        global sample_3
        two_to_three = sample_2.align_sequence(sample_3)
        three_to_two = sample_3.align_sequence(sample_2)
        self.assertEqual(two_to_three, three_to_two)
        self.assertEqual(two_to_three, 51)

if __name__ == '__main__':
    unittest.main()
