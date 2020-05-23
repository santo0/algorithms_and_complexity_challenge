'''
    Title: seq_align_tests.py
    Author: Guillem Camats Felip, Adria Juve Sanchez, Marti La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
import unittest
from preprocessing import MedianSample

SEQ_1 = 'ATTAAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTC'+\
        'TTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGCTGTCACTC'+\
        'GGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC'
SEQ_2 = 'ATTAAAGGTTTATACCTTCCAACAAACCAACCAAATCTCTTGTAGATCTC'+\
        'TAAACGAACATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGCACTCA'+\
        'CGCAGTATAATTAATAAC'
SEQ_3 = 'TTCGATCTACTTGTAGATCTAGTTCTCTAAACGAACTTTAAAATCTGTGT'+\
        'GGAAAACTGTCACTCGGCTGCATGCTTAGTGCAACGTACGTNACT'
SAMPLE_1 = MedianSample('SANTA',
                        '12/25/XX',
                        'North Pole',
                        sequence=SEQ_1)
SAMPLE_2 = MedianSample('SATAN',
                        '6/6/6',
                        'Helvetti',
                        sequence=SEQ_2)
SAMPLE_3 = MedianSample('SANTANA',
                        '4/20/20',
                        'Mexico',
                        sequence=SEQ_3)

class SeqAlignTesting(unittest.TestCase):
    '''Unit test of sequence alignment'''
    def test_seq_align_1(self):
        '''Test of sequence alignment between seq_1 and seq_2'''
        score_1 = SAMPLE_1.align_sequence(SAMPLE_2)
        score_2 = SAMPLE_2.align_sequence(SAMPLE_1)
        self.assertEqual(score_1, score_2)
        self.assertEqual(score_1, 22)

    def test_seq_align_2(self):
        '''Test of sequence alignment between seq_1 and seq_3'''
        score_1 = SAMPLE_1.align_sequence(SAMPLE_3)
        score_2 = SAMPLE_3.align_sequence(SAMPLE_1)
        self.assertEqual(score_1, score_2)
        self.assertEqual(score_1, 60)

    def test_seq_align_3(self):
        '''Test of sequence alignment between seq_2 and seq_3'''
        score_1 = SAMPLE_2.align_sequence(SAMPLE_3)
        score_2 = SAMPLE_3.align_sequence(SAMPLE_2)
        self.assertEqual(score_1, score_2)
        self.assertEqual(score_1, 51)

if __name__ == '__main__':
    unittest.main()
