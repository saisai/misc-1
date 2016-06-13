#include <Python.h>


int main(int argc, char *argv[])
{
    PyObject *d, *m, *v, *res;
    FILE *fp;
    char nm[512], *key;

    Py_SetProgramName(argv[1]);  /* optional but recommended */
    Py_Initialize();

    m = PyImport_AddModule("dummy");
    if (m == NULL)
        return 1;
    PyModule_AddObject(m, "__builtins__",
                       PyImport_ImportModule("__builtin__"));

    d = PyModule_GetDict(m);

    key = getenv("KEY");
    if (key == NULL) {
        printf("No KEY set\n");
        return 1;
    }
    fp = fopen("enc.x", "rb");
    fread(nm, sizeof(char), 304, fp);
    PyDict_SetItemString(d, "enc", PyString_FromStringAndSize(nm, 304));
    PyDict_SetItemString(d, "key", PyString_FromString(key));
    v = PyRun_String(
"import hashlib\n"
"from Crypto.Cipher import AES\n"
"cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_CBC, enc[:16])\n"
"dec = cipher.decrypt(enc[16:])\n"
"res = dec[:-ord(dec[-1])]\n",
                                Py_file_input, d, d);
    if (v == NULL) {
        PyErr_Print();
        return 1;
    }
    printf("RESULT: %s\n",
           PyString_AsString(PyDict_GetItemString(d, "res")));
    Py_DECREF(v);

    Py_Finalize();
    return 0;
}
