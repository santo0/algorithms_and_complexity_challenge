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
import random
import alignment
from ctypes import cdll, c_int, c_char_p

lib = cdll.LoadLibrary("alignment_rust/target/release/libalignment_rust.so")
lib.alignment.argtypes = (c_char_p, c_char_p)
lib.alignment.restype = c_int

MAX_ALIGN_LENGTH = 5000

class MedianSample():
    '''Sample of median length of a country'''

    def __init__(self, sample_id, date, geolocation, sequence=""):
        self.sample_id = sample_id
        self.date = date
        self.geolocation = geolocation
        self.sequence = sequence

    def set_fasta_sequence(self, fasta_sequence):
        '''Assign a sequence'''
        self.sequence = fasta_sequence

    def align_sequence(self, other_sample):
        '''Sets maximum length of sequence'''
        seq_1 = self.sequence[:MAX_ALIGN_LENGTH]
        seq_2 = other_sample.sequence[:MAX_ALIGN_LENGTH]
        max_score = alignment.alignment(seq_1, seq_2)
        return max_score

    def align_sequence_rust(self, other_sample):
        
        seq_1 = self.sequence[:MAX_ALIGN_LENGTH].encode()
        seq_2 = other_sample.sequence[:MAX_ALIGN_LENGTH].encode()
        max_score = lib.alignment(seq_1, seq_2)
        return max_score

    def __repr__(self):
        return 'MedianSample(id={i}, date={d}, geolocation={g})\n'.format(i=self.sample_id,
                                                                          d=self.date,
                                                                          g=self.geolocation)

def get_samples_alignement_matrix(samples_list):
    '''Get the matrix of scores of all sample alignments'''
    total_samples = len(samples_list)
    score_matrix = [[None for j in range(total_samples)]
                    for i in range(total_samples)]
    for i in range(total_samples):
        for j in range(total_samples):
            # Normalitzar per a q siguin coeficients entre -1 i 1
            if i == j:
                score_matrix[i][j] = 0
            else:
                if score_matrix[j][i] is None:
                    sample_1 = samples_list[i]
                    sample_2 = samples_list[j]
                    score_matrix[i][j] = sample_1.align_sequence(sample_2)
                else:
                    score_matrix[i][j] = score_matrix[j][i]
    return score_matrix

def get_rust_samples_alignement_matrix(samples_list):
    '''Get the matrix of scores of all sample alignments'''
    total_samples = len(samples_list)
    score_matrix = [[None for j in range(total_samples)]
                    for i in range(total_samples)]
    for i in range(total_samples):
        for j in range(total_samples):
            # Normalitzar per a q siguin coeficients entre -1 i 1
            if i == j:
                score_matrix[i][j] = 0
            else:
                if score_matrix[j][i] is None:
                    sample_1 = samples_list[i]
                    sample_2 = samples_list[j]
                    score_matrix[i][j] = sample_1.align_sequence_rust(sample_2)
                else:
                    score_matrix[i][j] = score_matrix[j][i]
    return score_matrix

def normalize_sample_alignment_matrix(score_matrix):
    '''Heatmap of score matrix'''
    total_samples = len(score_matrix)
    new_matrix = [[None for j in range(total_samples)]
                  for i in range(total_samples)]

    for i in range(total_samples):
        for j in range(total_samples):
            if i == j:
                new_matrix[i][j] = 1
            else:
                if new_matrix[j][i] is None:
                    new_matrix[i][j] = score_matrix[i][j] / \
                        max((score_matrix[i][i], score_matrix[j][j]))
                else:
                    new_matrix[i][j] = new_matrix[j][i]
    plt.imshow(new_matrix, cmap='hot', interpolation='nearest')
    plt.show()
    return new_matrix

def call_get_median(samples_list):
    '''Get_median of samples list'''
    return get_median(samples_list, len(samples_list) // 2)

def get_median(samples_list, samples_list_length):
    '''Get median of samples list'''
    sublists = [samples_list[i:i+5] for i in range(0, len(samples_list), 5)]
    medians = [sorted(sublist, key=itemgetter(2))[len(sublist)//2]
               for sublist in sublists]
    if len(medians) <= 5:
        pivot = sorted(medians)[len(medians)//2]
    else:
        pivot = get_median(medians, len(medians)//2)
    low = [i for i in samples_list if i[2] <= pivot[2]]
    low.remove(pivot)
    high = [i for i in samples_list if i[2] > pivot[2]]
    k = len(low)
    if samples_list_length < k:
        return get_median(low, samples_list_length)
    if samples_list_length > k:
        return get_median(high, samples_list_length-k-1)
    return pivot

def get_fasta_sequences(sample_list, dir_path):
    '''Obtain FASTA sequences from the web'''
    print("Getting fasta sequences from the web")
    for sample in sample_list:
        fasta_path = dir_path + sample.sample_id + ".fasta"
        if os.path.isfile(fasta_path):
            f_open = open(fasta_path)
            data = f_open.read()
            f_open.close()
        else:
            url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/' +\
                'efetch.fcgi?db=nucleotide&id={}&rettype=fasta'.format(
                    sample.sample_id)
            try:
                response = urllib.request.urlopen(url)
                # es suposa q larxiu donat correspon al id
                data = response.read().decode('utf-8')
            except urllib.error.HTTPError:
                print("sample whit id {} doesn't exist".format(sample.sample_id))
                sys.exit(1)
            f_open = open(fasta_path, '+w')
            f_open.write(data)
            f_open.close()
        splitted_data = data.split('\n')
        sample.sequence = ''.join(splitted_data[1:])
    print("Fasta sequences obtained")

def preprocess(csv_path):
    '''Classify data from csv file'''
    country_dict = {}

    csv_file = open(csv_path, "r")
    data_reader = csv.DictReader(csv_file)

    for row in data_reader:
        if row["Length"] != "" and\
                row["Accession"] != "" and\
                row["Release_Date"] != "" and\
                row["Geo_Location"] != "":
            values_tuples = (row["Accession"],
                             row["Release_Date"], int(row["Length"]))
            country_name = row["Geo_Location"].split(":")[0]
            if country_name in country_dict.keys():
                country_dict[country_name].append(values_tuples)
            else:
                country_dict[country_name] = [
                    values_tuples]
    csv_file.close()
    medians_list = []
    for country in country_dict:
        median_sample = call_get_median(country_dict[country])
        final_sample = MedianSample(
            median_sample[0], median_sample[1], country)
        medians_list.append(final_sample)
    return medians_list

def check_equal_cluster(newCluster,oldCluster):
    for key in newCluster.keys():
        if key not in oldCluster.keys() or set(newCluster[key])-set(oldCluster[key])!=set():
            return False
    return True

def calculate_min_puntuation(newCluster,score_matrix):
    newPoints=[]
    for key in newCluster.keys():
        new_min=-1
        for number in newCluster[key]:
            newPuntuation=0
            for i in range(0,len(newCluster[key])):
                newPuntuation+=score_matrix[number][newCluster[key][i]]
            if new_min==-1  or new_min>newPuntuation:
                new_min=newPuntuation
                new_min_number=number
        newPoints.append(new_min_number)
    return newPoints

def create_clustering(points,clusters,score_matrix):
    newClusters={str(point):[] for point in points}
    for i in range(0,len(score_matrix)):
        new_min=-1
        for point in points:
            if new_min==-1 or i==point or new_min>score_matrix[i][point]:
                new_min=score_matrix[i][point]
                closestPoint=point
        newClusters[str(closestPoint)].append(i)
    print(newClusters)
    if check_equal_cluster(newClusters,clusters):
        return newClusters
    else:
        return create_clustering(calculate_min_puntuation(newClusters,score_matrix),newClusters,score_matrix)

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
    median_sample_list = preprocess(csv_path)
    print("--- %s seconds for preprocessing csv ---" %
          (time.time() - start_time))
    start_time = time.time()
    get_fasta_sequences(median_sample_list, dir_path)
    print("--- %s seconds for getting fastas ---" % (time.time() - start_time))
    print(len(median_sample_list))
    print('Start score matrix')
    start_time = time.time()
    #score_matrix = get_samples_alignement_matrix(median_sample_list)
    #print(score_matrix)
    print("--- %s seconds for getting score matrix ---" %
          (time.time() - start_time))

    print('Start rust score matrix')
    start_time = time.time()
    rust_score_matrix = get_rust_samples_alignement_matrix(median_sample_list)
    print(rust_score_matrix)
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
