#define PY_SSIZE_T_CLEAN
#include </usr/include/python3.6m/Python.h>
/*
#def __init_gap_line__(self,partial_scoring_matrix,gap_penal):
    #    for x in range(len(partial_scoring_matrix[0])):
    #        partial_scoring_matrix[0][x]=x*gap_penal
    #    for y in range(len(partial_scoring_matrix)):
    #        partial_scoring_matrix[y][0]=y*gap_penal

    #def __compute_matrix__(self,compared_fasta_data,scoring_matrix,gap_penal):
    #    partial_scoring_matrix=np.empty([len(self.fasta)+1,len(compared_fasta_data)+1])
    #    partial_scoring_matrix=list(partial_scoring_matrix)
    #    a=0
        #partial_scoring_matrix=[ [] * len(self.fasta)+1 ] * (len(compared_fasta_data)+1
        #partial_scoring_matrix=[[0 for x in range(len(self.fasta)+1)] for y in range(len(compared_fasta_data)+1)]
    #    self.__init_gap_line__(partial_scoring_matrix,gap_penal)
        #range(1,len(compared_fasta_data)+1):
    #    for x in range(1,len(compared_fasta_data)+1):
    #        print(x)
    #        for y in range(1,len(self.fasta)+1):
    #            equal=partial_scoring_matrix[x-1][y-1]+1#scoring_matrix[compared_fasta_data[x-1]][self.fasta[y-1]]
    #            first_sequence_gap=partial_scoring_matrix[x-1][y]+gap_penal
    #            second_sequence_gap=partial_scoring_matrix[x][y-1]+gap_penal
                #partial_scoring_matrix[x][y]=max([equal,first_sequence_gap,second_sequence_gap])
    #    return partial_scoring_matrix

    #def align_sequence(self,compared_fasta_data,scoring_matrix,gap_penal):
    #    partial_scoring_matrix=self.__compute_matrix__(compared_fasta_data,scoring_matrix,gap_penal)
    #    maxScore=partial_scoring_matrix[len(partial_scoring_matrix)-1][len(partial_scoring_matrix[0])-1]
    #    print("Hola")
*/

void initGapLine(int **matrix,int xlen,int ylen,int gapPenal){
    int y;
    int x;
    for(y=0;y<ylen+1;y+=1){
        matrix[y][0]=y*gapPenal;
    }
    for(x=0;x<xlen+1;x+=1){
        matrix[0][x]=x*gapPenal;
    }
}

int getNucleoidData(char compareChar,char comparedChar,int **matrix){
    printf("compareChar %c \n",compareChar);
    printf("ComparedChar %c \n",comparedChar);
    switch(compareChar)
    {
        case 'A':
            switch (comparedChar)
            {
            case 'A':
                return matrix[0][0];
                break;
            case 'T':
                return matrix[0][1];
                break;
            case 'C':
                return matrix[0][2];
                break;
            case 'G':
                return matrix[0][3];
                break;
            default:
                return 0;
                break;
            }
            break;
        case 'T':
            switch (comparedChar)
            {
            case 'A':
                return matrix[1][0];
                break;
            case 'T':
                return matrix[1][1];
                break;
            case 'C':
                return matrix[1][2];
                break;
            case 'G':
                return matrix[1][3];
                break;
            default:
                return 0;
                break;
            }
            break;
        case 'C':
            switch (comparedChar)
            {
            case 'A':
                return matrix[2][0];
                break;
            case 'T':
                return matrix[2][1];
                break;
            case 'C':
                return matrix[2][2];
                break;
            case 'G':
                return matrix[2][3];
                break;
            default:
                return 0;
                break;
            }
            break;
        case 'G':
            switch (comparedChar)
            {
            case 'A':
                return matrix[3][0];
                break;
            case 'T':
                return matrix[3][1];
                break;
            case 'C':
                return matrix[3][2];
                break;
            case 'G':
                printf("Hola %i \n",matrix[3][3]);
                return matrix[3][3];
                break;
            default:
                return 0;
                break;
            }
            break;
        default:
            return 0;
    }
}

int max(int firstNumber,int secondNumber){
    return (firstNumber>secondNumber)?firstNumber:secondNumber;
}
int computeMatrix(char* sequence1,char* sequence2,int **matrix,int gapPenal)
{   
    int xlen=strlen(sequence1);
    int ylen=strlen(sequence2);
    int partial_scoring_matrix[ylen+1][xlen+1];
    initGapLine(partial_scoring_matrix,xlen,ylen,gapPenal);
    for(int yIndex=1;yIndex<ylen+1;yIndex+=1){
        for(int xIndex=1;xIndex<xlen+1;xIndex+=1){
            int equal=partial_scoring_matrix[yIndex-1][xIndex-1]+getNucleoidData(sequence1[xIndex-1],sequence2[yIndex-1],matrix);
            int firstSequenceGap=partial_scoring_matrix[yIndex-1][xIndex]+gapPenal;
            int secondSequenceGap=partial_scoring_matrix[yIndex][xIndex-1]+gapPenal;
            partial_scoring_matrix[yIndex][xIndex]=max(max(equal,firstSequenceGap),secondSequenceGap);
        }
    }
}
static PyObject * alignment_function(PyObject *self, PyObject *args)
{
    const char *sequence1;
    const char *sequence2;
    if (!PyArg_ParseTuple(args, "ss", &sequence1,&sequence2)){
        return NULL;
    }
    int scoringMatrix[4][4]={{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}};
    int gapPenal=0;
    return PyLong_FromLong(computeMatrix(sequence1,sequence2,scoringMatrix,gapPenal));
}

static PyMethodDef alignmentMethods[] = {
    {"alignment",  alignment_function, METH_VARARGS,
     "Executes sequence alignment via the Needleman-Wunsch algorithm"}
};

static struct PyModuleDef alignmentmodule = {
    PyModuleDef_HEAD_INIT,
    "alignment",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    alignmentMethods
};

PyMODINIT_FUNC PyInit_alignment(void)
{
    return PyModule_Create(&alignmentmodule);
}