import sys
import optparse
from optparse import OptionParser
import os.path
import logging
import csv
from operator import itemgetter


class MedianSample():

    def __init__(self, id, date, geolocation, fasta_sequence=""):
        self.id = id
        self.date = date
        self.geolocation = geolocation
        self.fasta = fasta_sequence
        
    def set_fasta_sequence(self, fasta_sequence):
        self.fasta = fasta_sequence
    
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

def get_fasta_sequences(fasta_file_name, sample_list):              
    fasta_file = open(fasta_file_name, 'r')                             #Try/except¿?¿?
    all_fasta_samples = fasta_file.read().split('>')             #Saving all in memory, using split/There is another alternate option that uses less memory by doing line to line   
    fasta_file.close()
    for fasta_sample in all_fasta_samples:
        fasta_sample_splitted = fasta_sample.split('\n')            #We know that in the first elems there will be the fasta header
        fasta_sample_header = fasta_sample_splitted[0]              #This line can be in the next one
        fasta_sample_id = fasta_sample_header.split('|')[0]
        median_sample_with_id = get_median_sample_by_id(fasta_sample_id.strip(), sample_list)
        if median_sample_with_id:
            fasta_sample_sequence = ''.join([sequence_region.strip() for sequence_region in fasta_sample_splitted[1:]])
            median_sample_with_id.set_fasta_sequence(fasta_sample_sequence)
            
                                                                    #In case that one or more MedianSample doesn't have fasta_sequence
                                                                    #Exit program
def get_median_sample_by_id(sample_id, sample_list):
    for sample in sample_list:
        if sample_id == sample.id:
            return sample
    return None 

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
    parser.add_option('-d','--debug',dest = "debug", action='store_true',default=False,help='debug mode')
    parser.add_option("-c", "--csv", dest="csv", default = './sequences.csv',help="path of csv file")
    parser.add_option("-f", "--fasta", dest="fasta", default = './sequences_fasta.fasta', help="path of fasta file")
    (options, args) = parser.parse_args()
    if not (os.path.isfile(options.csv) and os.path.isfile(options.fasta)):
        sys.exit(1)
    logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s',datefmt="%y/%m/%d/-%H:%M:%S",level=logging.INFO)    
    if options.debug:
        logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s',datefmt="%y/%m/%d/-%H:%M:%S",level=logging.DEBUG)
    csv_path = options.csv
    fasta_path = options.fasta
    median_sample_list = preprocess(csv_path)
    get_fasta_sequences(fasta_path, median_sample_list)
