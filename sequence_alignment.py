'''
    Title: sequence_alignment.py
    Author: Guillem Camats Felip, Adrià Juvé Sánchez, Martí La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
from dec_timer import timer

@timer
def get_samples_alignment_matrix(samples_list, alignment_language):
    '''Get the matrix of scores of all sample alignments'''
    total_samples = len(samples_list)
    score_matrix = [[None for j in range(total_samples)]
                    for i in range(total_samples)]
    for i in range(total_samples):
        for j in range(total_samples):
            if i == j:
                score_matrix[i][j] = 0
            else:
                if score_matrix[j][i] is None:
                    sample_1 = samples_list[i]
                    sample_2 = samples_list[j]
                    if alignment_language:
                        score_matrix[i][j] = sample_1.align_sequence(sample_2)
                    else:
                        score_matrix[i][j] = sample_1.align_sequence_rust(sample_2)
                else:
                    score_matrix[i][j] = score_matrix[j][i]
    return score_matrix
