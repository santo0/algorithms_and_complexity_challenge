import sys
import optparse
from optparse import OptionParser
import os.path
import logging
import csv
from operator import itemgetter
import urllib
import urllib.request
import alignment

class MedianSample():

    def __init__(self, id, date, geolocation, fasta_sequence=""):
        self.id = id
        self.date = date
        self.geolocation = geolocation
        self.fasta = fasta_sequence
        
    def set_fasta_sequence(self, fasta_sequence):
        self.fasta = fasta_sequence
        
    def align_sequence(self,compared_fasta_data):
        maxScore=alignment.alignment(self.fasta,compared_fasta_data)
        print(maxScore)
    
    def get_fasta(self):
        return self.fasta

    def __repr__(self):
        return 'MedianSample(id={i}, date={d}, geolocation={g})\n'.format(i=self.id, d=self.date, g=self.geolocation)

def call_get_median(samples_list):
    return get_median(samples_list, len(samples_list) // 2)

def get_median(samples_list, samples_list_length):
    sublists = [samples_list[i:i+5] for i in range(0, len(samples_list), 5)]
    medians = [sorted(sublist, key=itemgetter(2))[len(sublist)//2] for sublist in sublists]
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
    elif samples_list_length > k:
        return get_median(high, samples_list_length-k-1)
    else:
        return pivot

def get_fasta_sequences(sample_list):
    print("getting fasta sequences from the web")          
    for sample in sample_list:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id={}&rettype=fasta'.format(sample.id)
        try: 
            response = urllib.request.urlopen(url)
            data = response.read().decode('utf-8')#es suposa q larxiu donat correspon al id
        except urllib.error.HTTPError:
            print("sample whit id {} doesn't exist".format(sample.id))
            answer = ''
            while not(answer == 'yes' or answer == 'no'):
                answer = input("exit program? yes / no\n")
                if answer == 'yes':
    	            sys.exit(1)            
        splitted_data = data.split('\n')
        sample.fasta = ''.join(splitted_data[1:])
    print("fasta sequences obtined")    





#Function that reads a csv file and calculates the median of each country.
def preprocess(csv_path):
    country_dict = {}

    csv_file = open(csv_path, "r")
    data_reader = csv.DictReader(csv_file)

    for row in data_reader:
        if row["Length"] != "" and row["Accession"] != "" and row["Release_Date"] != "" and row["Geo_Location"] != "":
            values_tuples = (row["Accession"],row["Release_Date"], int(row["Length"]))
            if row["Geo_Location"].split(":")[0] in country_dict.keys():
                
                country_dict[row["Geo_Location"].split(":")[0]].append(values_tuples)
            else:
                country_dict[row["Geo_Location"].split(":")[0]] = [values_tuples]
    
    csv_file.close()   

    medians_list = []
    for country in country_dict.keys():       
        median_sample = call_get_median(country_dict[country])
        final_sample = MedianSample(median_sample[0], median_sample[1],country)
        medians_list.append(final_sample)
    return medians_list


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-c", "--csv", dest="csv", default = './sequences.csv',help="path of csv file")
    (options, args) = parser.parse_args()
    if not (os.path.isfile(options.csv)):
        sys.exit(1)
    csv_path = options.csv
    median_sample_list = preprocess(csv_path)
    get_fasta_sequences(median_sample_list)
    median_sample_list[0].align_sequence(median_sample_list[1].get_fasta())
