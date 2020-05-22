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
import csv
from operator import itemgetter
import urllib
import urllib.request
import time
import matplotlib.pyplot as plt
import alignment
import random
from preprocessing import get_samples_of_median_length_by_country, get_fasta_sequences
from sequence_alignement import get_samples_alignement_matrix
from classify import create_clustering
import networkx as nx


def main():
    '''Get arguments and calls main functions'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        dest='dir',
                        default='',
                        help='relative path of directory of csv and fasta.\n'+\
                        'Exemple: ./sarscovhierarchy.py -d data_set/ ')
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
    score_matrix = get_samples_alignement_matrix(median_sample_list)
    print(score_matrix)
    print("--- %s seconds for getting score matrix ---" %
          (time.time() - start_time))
    final_clusters = clustering(median_sample_list, score_matrix)
    Tree = nx.Graph()
    #countries = []
    #for sample in median_sample_list:
    #    countries.append(sample.geolocation)
    #Tree.add_nodes_from(countries)
    Tree.add_node('Za Warudo')
    for medoid in final_clusters:
        Tree.add_node(medoid)
        Tree.add_edge('Centre', medoid)
        for country in final_clusters[medoid]:
            Tree.add_node(country)
            Tree.add_edge(medoid, country)
    nx.draw(Tree, with_labels=True, font_size = '6') 
    plt.show()   

def clustering(median_sample_list, score_matrix):
    points = []
    i = 0
    while i < 6:
        element = random.randrange(0, 30, 1)
        if element not in points:
            points.append(element)
            i += 1
    clustering_with_geolocalitation = {}
    resultClusters=create_clustering(points, {}, score_matrix)
    for key in resultClusters.keys():
        clustering_with_geolocalitation.update({median_sample_list[int(key)].geolocation:[]})
        for value in resultClusters[key]:
            clustering_with_geolocalitation[median_sample_list[int(key)].geolocation].append(median_sample_list[value].geolocation)
    return clustering_with_geolocalitation

if __name__ == "__main__":
    main()
