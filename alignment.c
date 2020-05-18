#define PY_SSIZE_T_CLEAN
#include </usr/include/python3.7m/Python.h>

int min(int firstNumber,int secondNumber){
    return (firstNumber>secondNumber)?secondNumber:firstNumber;
}

int computeMatrix(char* sequence1,char* sequence2)
{   
    int xlen=strlen(sequence1);
    int ylen=strlen(sequence2);
    int* partial_scoring_matrix=NULL;
    partial_scoring_matrix=malloc((ylen+1)*(xlen+1)*sizeof(int));
    int y;
    int x;
    for(y=0;y<ylen+1;y+=1){
        *(partial_scoring_matrix+y*(xlen+1))=y;
    }
    for(x=0;x<xlen+1;x+=1){
        *(partial_scoring_matrix+x)=x;
    }
    
    for(int yIndex=1;yIndex<ylen+1;yIndex+=1){
        for(int xIndex=1;xIndex<xlen+1;xIndex+=1){
            int equal=*(partial_scoring_matrix+((yIndex-1)*(xlen+1))+(xIndex-1))+((sequence1[xIndex-1]==sequence2[yIndex-1])?0:1);
            int firstSequenceGap=*(partial_scoring_matrix+((yIndex-1)*(xlen+1))+xIndex)+1;
            int secondSequenceGap=*(partial_scoring_matrix+(yIndex*(xlen+1))+(xIndex-1))+1;
            *(partial_scoring_matrix+(yIndex*(xlen+1))+xIndex)=min(min(equal,firstSequenceGap),secondSequenceGap);
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
    return PyLong_FromLong(computeMatrix(sequence1,sequence2));
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