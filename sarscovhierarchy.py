import csv
from operator import itemgetter


class MedianSample():
    def __init__(self, id, date, geolocation, fasta_sequence=""):
        self.id = id
        self.date = date
        self.geolocation = geolocation
        self.fasta = fasta_sequence

    def __repr__(self):
        return 'MedianSample(id={i}, date={d}, geolocation={g})\n'.format(i=self.id, d=self.date, g=self.geolocation)

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
        country_dict[country] = sorted(country_dict[country], key=itemgetter(2))

        length = len(country_dict[country])
        correct_position = length // 2
        
        median_sample = country_dict[country][correct_position]
        final_sample = MedianSample(median_sample[0], median_sample[1], country)
        medians_list.append(final_sample)

    return medians_list


if __name__ == "__main__":
    csv_path = "/home/xavi_nadal/Documents/sequences.csv"
    print(preprocess(csv_path))