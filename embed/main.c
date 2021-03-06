#include <Python.h>


static PyObject *decrypt(PyObject *enc, const char *passphrase)
{
    static PyObject *res;
    PyObject *d, *m;

    m = PyImport_AddModule("dummy");
    if (m == NULL)
        return NULL;
    PyModule_AddObject(m, "__builtins__",
                       PyImport_ImportModule("__builtin__"));

    d = PyModule_GetDict(m);

    PyDict_SetItemString(d, "enc", enc);
    PyDict_SetItemString(d, "passphrase", PyString_FromString(passphrase));

    if (PyRun_String(
"import hashlib\n"
"from Crypto.Cipher import AES\n"
"key = hashlib.sha256(passphrase).digest()\n"
"cipher = AES.new(key, AES.MODE_CBC, enc[:16])\n"
"dec = cipher.decrypt(enc[16:])\n"
"res = dec[:-ord(dec[-1])]\n",
                     Py_file_input, d, d) == NULL) {
        PyErr_Print();
        return NULL;
    }
    res = PyDict_GetItemString(d, "res");
    if (res == NULL)
        return NULL;
    return res;
}


int main(int argc, char *argv[])
{
    PyObject *enc, *dec;
    FILE *fp;
    char buf[1024], *passphrase;

    passphrase = getenv("PASSPHRASE");
    if (passphrase == NULL) {
        printf("No PASSPHRASE set\n");
        return 1;
    }
    fp = fopen("enc.x", "rb");
    fread(buf, sizeof(char), 304, fp);

    Py_SetProgramName(argv[1]);  /* optional but recommended */
    Py_Initialize();

    enc = PyString_FromStringAndSize(buf, 304);

    dec = decrypt(enc, passphrase);
    if (dec == NULL) {
        printf("Error occured!\n");
        return 1;
    }
    printf("RESULT: %s\n", PyString_AsString(dec));

    Py_Finalize();
    return 0;
}
