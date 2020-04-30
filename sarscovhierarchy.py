class MedianSample():
    def __init__(self, id, date, geolocation,fasta_sequence=""):
        self.id = id
        self.date = date
        self.geolocation = geolocation
        self.fasta = fasta_sequence

    def set_fasta_sequence(self, fasta_sequence):
        self.fasta = fasta_sequence
    
    def __repr__(self):
        return 'MedianSample(id={i}, date={d}, geolocation={g})\n'.format(i=self.id, d=self.date, g=self.geolocation)
    

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
        print(sample_id, sample.id, sample_id == sample.id)
        if sample_id == sample.id:
            return sample
    return None
