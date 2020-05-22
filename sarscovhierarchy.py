'''
    Title: sarscovhierarchy.py
    Author: Guillem Camats Felip, Adrià Juvé Sánchez, Martí La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
import sys
import argparse
import os.path
import time
import matplotlib.pyplot as plt
import networkx as nx
from preprocessing import get_samples_of_median_length_by_country, get_fasta_sequences
from sequence_alignment import get_samples_alignment_matrix
from classify import clustering


def main():
    '''Get arguments and calls main functions'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        dest='dir',
                        default='',
                        help='relative path of directory of csv and fasta.\n' +
                        'Exemple: ./sarscovhierarchy.py -d data_set/ ')
    parser.add_argument('-r', '--rust', action='store_true',
                        default=False, help='Activate rust algorithm (not recommended)')
    rust_activated = parser.parse_args().rust

    args = parser.parse_args()
    dir_path = args.dir
    if not os.path.isdir(dir_path):
        sys.exit(1)
    csv_path = dir_path + 'sequences.csv'
    start_time = time.time()
    median_sample_list = get_samples_of_median_length_by_country(csv_path)
    print("--- %s seconds for preprocessing csv ---" %
          (time.time() - start_time))
    start_time = time.time()
    get_fasta_sequences(median_sample_list, dir_path)
    print("--- %s seconds for getting fastas ---" % (time.time() - start_time))
    print(len(median_sample_list))
    print('Start score matrix')
    start_time = time.time()
    if not rust_activated:
        score_matrix = get_samples_alignment_matrix(median_sample_list, True)
    else:
        score_matrix = get_samples_alignment_matrix(median_sample_list, False)
    print(score_matrix)
    print("--- %s seconds for getting score matrix ---" %
          (time.time() - start_time))
    final_clusters = clustering(median_sample_list, score_matrix)
    draw_cluster_map(final_clusters)


def draw_cluster_map(final_clusters):
    '''Shows graphical representation of clustering'''
    tree = nx.Graph()
    for medoid in final_clusters:
        tree.add_node(medoid)
        tree.add_edge('Centre', medoid)
        for country in final_clusters[medoid]:
            tree.add_node(country)
            tree.add_edge(medoid, country)
    nx.draw(tree, with_labels=True, font_size='6')
    plt.show()


if __name__ == "__main__":
    main()
