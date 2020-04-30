import sys
import optparse
from optparse import OptionParser
import os.path
import logging

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
    