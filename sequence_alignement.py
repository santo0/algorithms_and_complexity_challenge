'''
    Title: sequence_alignement.py
    Author: Guillem Camats Felip, Adrià Juvé Sánchez, Martí La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
import time
from preprocessing import MedianSample


def get_samples_alignement_matrix(samples_list):
    '''Get the matrix of scores of all sample alignments'''
    total_samples = len(samples_list)
    score_matrix = [[None for j in range(total_samples)]
                    for i in range(total_samples)]
    for i in range(total_samples):
        print('>>>>>>>>>>>>>Start {}'.format(i))
        start = time.time()
        for j in range(total_samples):
            other_start = time.time()
            if i == j:
                score_matrix[i][j] = 0
            else:
                if score_matrix[j][i] is None:
                    sample_1 = samples_list[i]
                    sample_2 = samples_list[j]
                    score_matrix[i][j] = sample_1.align_sequence(sample_2)
                else:
                    score_matrix[i][j] = score_matrix[j][i]
            print('{} with {}, duration = {}'.format(i, j, time.time() - other_start))
        print('>>>>>>>>>>>>>Finish {}, duration = {}'.format(i, time.time() - start))
    return score_matrix
