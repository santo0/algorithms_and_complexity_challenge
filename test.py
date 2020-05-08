def init_gap_line(partial_scoring_matrix,gap_penal):
        for x in range(len(partial_scoring_matrix[0])):
            partial_scoring_matrix[0][x]=x*gap_penal
        for y in range(len(partial_scoring_matrix)):
            partial_scoring_matrix[y][0]=y*gap_penal

def compute_matrix(self_fasta,compared_fasta_data,scoring_matrix,gap_penal):
    partial_scoring_matrix=[[0 for x in range(len(self_fasta)+1)] for y in range(len(compared_fasta_data)+1)]
    init_gap_line(partial_scoring_matrix,gap_penal)
    for x in range(1,len(compared_fasta_data)+1):
        for y in range(1,len(self_fasta)+1):
            equal=partial_scoring_matrix[x-1][y-1]+scoring_matrix[compared_fasta_data[x-1]][self_fasta[y-1]]
            first_sequence_gap=partial_scoring_matrix[x-1][y]+gap_penal
            second_sequence_gap=partial_scoring_matrix[x][y-1]+gap_penal
            partial_scoring_matrix[x][y]=max([equal,first_sequence_gap,second_sequence_gap])
    return partial_scoring_matrix

def getalignments(partial_scoring_matrix):
    new_sequence_A=""
    new_sequence_B=""

def align_sequence(self_fasta,compared_fasta_data,scoring_matrix,gap_penal):
    partial_scoring_matrix=compute_matrix(self_fasta,compared_fasta_data,scoring_matrix,gap_penal)
    maxScore=partial_scoring_matrix[len(partial_scoring_matrix)-1][len(partial_scoring_matrix[0])-1]
    print(partial_scoring_matrix)
    print(maxScore)

    
scoring_matrix={"A":{"A":1,"T":0,"C":0,"G":0},"T":{"A":0,"T":1,"C":0,"G":0},"C":{"A":0,"T":0,"C":1,"G":0},"G":{"A":0,"T":0,"C":0,"G":1}}
gap_penal=0
self_fasta="GAATTCAGTTA"
compared_fasta_data="GGATCGA"
align_sequence(self_fasta,compared_fasta_data,scoring_matrix,gap_penal)