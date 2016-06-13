#include <Python.h>


int main(int argc, char *argv[])
{
    PyObject *d, *m, *v, *bar;

    Py_SetProgramName(argv[1]);  /* optional but recommended */
    Py_Initialize();

    m = PyImport_AddModule("wnci128275909");
    if (m == NULL)
        return 1;
    PyModule_AddObject(m, "__builtins__",
                       PyImport_ImportModule("__builtin__"));

    d = PyModule_GetDict(m);
    PyDict_SetItemString(d, "foo", PyInt_FromLong(42));
    v = PyRun_String("import os\n"
                     "from Crypto import Random\n"
                     "print os, foo\n"
                     "bar = foo ** 3\n",
                     Py_file_input, d, d);
    if (v == NULL) {
        PyErr_Print();
        return 1;
    }
    bar = PyDict_GetItemString(d, "bar");
    printf("RESULT: %ld\n", PyLong_AsLong(bar));
    Py_DECREF(v);

    Py_Finalize();
    return 0;
}
