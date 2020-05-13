#define PY_SSIZE_T_CLEAN
#include </usr/include/python3.7m/Python.h>

int getNucleoidData(char compareChar,char comparedChar,int matrix[4][4]){
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
    return (firstNumber<secondNumber)?secondNumber:firstNumber;
}
int computeMatrix(char* sequence1,char* sequence2,int matrix[4][4],int gapPenal)
{   
    int xlen=strlen(sequence1);
    int ylen=strlen(sequence2);
    int* partial_scoring_matrix=NULL;
    partial_scoring_matrix=malloc((ylen+1)*(xlen+1)*sizeof(int));
    int y;
    int x;
    for(y=0;y<ylen+1;y+=1){
        *(partial_scoring_matrix+y*(xlen+1)+0)=y*gapPenal;
    }
    for(x=0;x<xlen+1;x+=1){
        *(partial_scoring_matrix+0+x)=x*gapPenal;
    }
    
    for(int yIndex=1;yIndex<ylen+1;yIndex+=1){
        for(int xIndex=1;xIndex<xlen+1;xIndex+=1){
            int equal=*(partial_scoring_matrix+((yIndex-1)*(xlen+1))+(xIndex-1))+getNucleoidData(sequence1[xIndex-1],sequence2[yIndex-1],matrix);
            int firstSequenceGap=*(partial_scoring_matrix+((yIndex-1)*(xlen+1))+xIndex)+gapPenal;
            int secondSequenceGap=*(partial_scoring_matrix+(yIndex*(xlen+1))+(xIndex-1))+gapPenal;
            *(partial_scoring_matrix+(yIndex*(xlen+1))+xIndex)=max(max(equal,firstSequenceGap),secondSequenceGap);
        }
    }
    int returnedValue=*(partial_scoring_matrix+(ylen*(xlen+1))+xlen);
    free(partial_scoring_matrix);
    return returnedValue;
}

static PyObject * alignment_function(PyObject *self, PyObject *args)
{
    char *sequence1;
    char *sequence2;
    if (!PyArg_ParseTuple(args, "ss", &sequence1,&sequence2)){
        return NULL;
    }
    int scoringMatrix[4][4]={{10,-4,-3,-1},{-4,8,0,-4},{-3,0,9,-5},{-1,-3,-5,7}};
    int gapPenal=-5;
    return PyLong_FromLong(computeMatrix(sequence1,sequence2,scoringMatrix,gapPenal));
}

static PyObject * max_alignment_value(PyObject *self, PyObject *args)
{
    char *sequence1;
    if (!PyArg_ParseTuple(args, "s", &sequence1)){
        return NULL;
    }
    int scoringMatrix[4][4]={{10,-4,-3,-1},{-4,8,0,-4},{-3,0,9,-5},{-1,-3,-5,7}};
    int maxPuntuation=0;
    int xlen=strlen(sequence1);
    for(int i=0;i<xlen;i+=1){
        maxPuntuation=maxPuntuation+getNucleoidData(sequence1[i],sequence1[i],scoringMatrix);
    }
    return PyLong_FromLong(maxPuntuation);
}

static PyMethodDef alignmentMethods[] = {
    {"alignment",  alignment_function, METH_VARARGS,
     "Executes sequence alignment via the Needleman-Wunsch algorithm"},
    {"max_alignment",  max_alignment_value, METH_VARARGS,
     "Calculates the max alignment value"} 
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