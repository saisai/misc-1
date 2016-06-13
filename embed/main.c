#include <Python.h>


int main(int argc, char *argv[])
{
    PyObject *d, *m, *v, *res;
    FILE *fp;
    char nm[512];

    Py_SetProgramName(argv[1]);  /* optional but recommended */
    Py_Initialize();

    m = PyImport_AddModule("wnci128275909");
    if (m == NULL)
        return 1;
    PyModule_AddObject(m, "__builtins__",
                       PyImport_ImportModule("__builtin__"));

    d = PyModule_GetDict(m);

    fp = fopen("enc.x", "rb");
    fread(nm, sizeof(char), 304, fp);
    PyDict_SetItemString(d, "enc", PyString_FromStringAndSize(nm, 304));
    PyDict_SetItemString(d, "key", PyString_FromString(getenv("PASSWORD")));
    v = PyRun_String(
            "import hashlib\n"
            "from Crypto.Cipher import AES\n"
            "KEY = hashlib.sha256(key).digest()\n"
            "cipher = AES.new(KEY, AES.MODE_CBC, enc[:16])\n"
            "res = cipher.decrypt(enc[16:])\n"
            "pad_len = ord(res[len(res) - 1:])\n"
            "res = res[:-pad_len]\n",
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
