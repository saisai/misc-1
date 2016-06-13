#include <Python.h>

int main(int argc, char *argv[])
{
    PyObject *d, *m, *v;

    Py_SetProgramName(argv[0]);  /* optional but recommended */
    Py_Initialize();

    m = PyImport_AddModule("cio_128275909");
    if (m == NULL)
        return 1;
    PyModule_AddObject(m, "__builtins__",
                       PyImport_ImportModule("__builtin__"));

    d = PyModule_GetDict(m);
    v = PyRun_String("import os\n"
                     "print os\n"
                     "from Crypto import Random\n",
                     Py_file_input, d, d);
    if (v == NULL) {
        PyErr_Print();
        return 1;
    }
    Py_DECREF(v);


    Py_Finalize();
    return 0;
}
