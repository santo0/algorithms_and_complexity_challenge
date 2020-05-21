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
    
    points=[]
    i=0
    while i<6:
        element=random.randrange(0,30,1)
        if element not in points:
            points.append(element)
            i+=1
    print(points)
    clustering=[[0,1,4,7,8,3],[1,0,3,6,5,2],[4,3,0,3,4,3],[7,6,3,0,5,4],[6,5,4,5,0,3],[3,2,3,4,3,0]]
    resultClusters=create_clustering([1,4],{},clustering)
    print(resultClusters)
    

if __name__ == "__main__":
    main()
