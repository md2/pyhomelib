#include <stdio.h>
#include <sqlite3.h>

#include <Python.h>

static PyObject *
sqlite3ext_load_icu(PyObject *self, PyObject *args)
{
	PyObject *obj;
	if (!PyArg_ParseTuple(args, "O", &obj))
		return NULL;
	sqlite3 *conn = *(sqlite3 **)PyCObject_AsVoidPtr(obj);
	sqlite3_enable_load_extension(conn, 1);
	int rc;
	char *err;
	if ((rc=sqlite3_load_extension(conn, "./libSqliteIcu.so", NULL, &err)) != SQLITE_OK) {
		fprintf(stderr, "Error: %d: %s\n", rc, err);
		sqlite3_free(err);
	}
	return (PyObject *)Py_BuildValue("");
}

static PyMethodDef
sqlite3extMethods[] =
{
	{ "load_icu", sqlite3ext_load_icu, METH_VARARGS },
	{ NULL, NULL },
};

void initsqlite3ext()
{
	Py_InitModule("sqlite3ext", sqlite3extMethods);
}

