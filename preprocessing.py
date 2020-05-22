'''
    Title: preprocessing.py
    Author: Guillem Camats Felip, Adrià Juvé Sánchez, Martí La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
import sys
import os.path
import csv
from operator import itemgetter
import urllib
import urllib.request
import alignment

MAX_ALIGN_LENGTH = 1000


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

    def __repr__(self):
        return 'MedianSample(id={i}, date={d}, geolocation={g})\n'.format(i=self.sample_id,
                                                                          d=self.date,
                                                                          g=self.geolocation)


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


def get_samples_of_median_length_by_country(csv_path):
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
