#include <Python.h>
#include <stdlib.h>

typedef struct {
    PyObject_HEAD
    int *data;
    int size;
    int capacity;
} DynamicArrayObject;

static void
DynamicArray_dealloc(DynamicArrayObject *self)
{
    free(self->data);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
DynamicArray_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    DynamicArrayObject *self;
    self = (DynamicArrayObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->data = (int *)malloc(10 * sizeof(int));
        self->size = 0;
        self->capacity = 10;
    }
    return (PyObject *)self;
}

static int
DynamicArray_init(DynamicArrayObject *self, PyObject *args, PyObject *kwds)
{
    return 0;
}

static PyObject *
DynamicArray_append(DynamicArrayObject *self, PyObject *args)
{
    int value;
    if (!PyArg_ParseTuple(args, "i", &value))
        return NULL;

    if (self->size == self->capacity) {
        self->capacity *= 2;
        self->data = (int *)realloc(self->data, self->capacity * sizeof(int));
    }

    self->data[self->size] = value;
    self->size++;
    Py_RETURN_NONE;
}

static PyObject *
DynamicArray_get(DynamicArrayObject *self, PyObject *args)
{
    int index;
    if (!PyArg_ParseTuple(args, "i", &index))
        return NULL;

    if (index < 0 || index >= self->size) {
        PyErr_SetString(PyExc_IndexError, "Index out of range");
        return NULL;
    }

    return PyLong_FromLong(self->data[index]);
}

static PyMethodDef DynamicArray_methods[] = {
    {"append", (PyCFunction)DynamicArray_append, METH_VARARGS, "Append an element to the array"},
    {"get", (PyCFunction)DynamicArray_get, METH_VARARGS, "Get an element from the array"},
    {NULL}
};

static PyTypeObject DynamicArrayType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "dynamicarray.DynamicArray",
    .tp_basicsize = sizeof(DynamicArrayObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor)DynamicArray_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = DynamicArray_new,
    .tp_init = (initproc)DynamicArray_init,
    .tp_methods = DynamicArray_methods,
};

static PyModuleDef dynamicarraymodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "dynamicarray",
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_dynamicarray(void)
{
    PyObject *m;
    if (PyType_Ready(&DynamicArrayType) < 0)
        return NULL;

    m = PyModule_Create(&dynamicarraymodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&DynamicArrayType);
    if (PyModule_AddObject(m, "DynamicArray", (PyObject *)&DynamicArrayType) < 0) {
        Py_DECREF(&DynamicArrayType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}

