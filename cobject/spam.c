#include <Python.h>

static PyObject *
spam_foo(PyObject *self, PyObject *args)
{
    static PyObject *cache = NULL;
    PyObject *key, *cobj;
    long i, j, *kptr;

    if (!PyArg_ParseTuple(args, "ii", &i, &j))
        return NULL;

    if (cache == NULL) {
        /* initialize cache */
        if ((cache = PyDict_New()) == NULL)
            return NULL;
    }

    /* build the key which is a tuple (i, j) */
    if ((key = Py_BuildValue("(ii)", i, j)) == NULL)
        return NULL;

    cobj = PyDict_GetItem(cache, key);
    if (cobj == NULL) {
        kptr = malloc(sizeof(kptr));
        *kptr = i + j;
        cobj = PyCObject_FromVoidPtr(kptr, NULL);
        if (PyDict_SetItem(cache, key, cobj) < 0)
            return NULL;
    }
    return Py_BuildValue("i", * (long *) PyCObject_AsVoidPtr(cobj));
}


static PyMethodDef SpamMethods[] = {
    {"foo", spam_foo, METH_VARARGS, "return the sum of two integers (cached)"},
    {NULL, NULL, 0, NULL}  /* Sentinel */
};


PyMODINIT_FUNC
initspam(void)
{
    (void) Py_InitModule("spam", SpamMethods);
}
