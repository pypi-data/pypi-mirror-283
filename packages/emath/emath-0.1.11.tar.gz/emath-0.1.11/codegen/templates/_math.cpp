
// generated from codegen/templates/_emath.cpp

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "_modulestate.hpp"
{% for type in vector_types %}
    #include "_{{ type.lower() }}.hpp"
{% endfor %}
{% for type in matrix_types %}
    #include "_{{ type.lower() }}.hpp"
{% endfor %}
{% for type in quaternion_types %}
    #include "_{{ type.lower() }}.hpp"
{% endfor %}
{% for type in pod_types %}
    #include "_{{ type.lower() }}.hpp"
{% endfor %}
#include "emath.h"


static PyMethodDef module_methods[] = {
    {0, 0, 0, 0}
};


static int
module_traverse(PyObject *self, visitproc visit, void *arg)
{
    ModuleState *state = (ModuleState *)PyModule_GetState(self);
    return ModuleState_traverse(state, visit, arg);
}


static int
module_clear(PyObject *self)
{
    ModuleState *state = (ModuleState *)PyModule_GetState(self);
    return ModuleState_clear(state);
}


static struct PyModuleDef module_PyModuleDef = {
    PyModuleDef_HEAD_INIT,
    "emath._math",
    0,
    sizeof(struct ModuleState),
    module_methods,
    0,
    module_traverse,
    module_clear
};


static void
api_destructor(PyObject *capsule)
{
    EMathApi* api = (EMathApi*)PyCapsule_GetPointer(
        capsule,
        "emath._math._api"
    );
    delete api;
}


PyMODINIT_FUNC
PyInit__math()
{
    auto api = new EMathApi{ 0 };
    auto api_capsule = PyCapsule_New(
        (void *)api,
        "emath._math._api",
        NULL
    );

    PyObject *module = PyModule_Create(&module_PyModuleDef);
    ModuleState *state = 0;
    if (!module){ goto error; }
    if (PyState_AddModule(module, &module_PyModuleDef) == -1){ goto error; }
    state = (ModuleState *)PyModule_GetState(module);

    {
        PyObject *ctypes = PyImport_ImportModule("ctypes");
        if (!ctypes){ goto error; }

        PyObject *ctypes_pointer = PyObject_GetAttrString(ctypes, "POINTER");
        if (!ctypes_pointer)
        {
            Py_DECREF(ctypes);
            goto error;
        }

        {% for c_type, ctypes_name in [
            ('bool', 'bool'),
            ('int8_t', 'int8'),
            ('uint8_t', 'uint8'),
            ('int16_t', 'int16'),
            ('uint16_t', 'uint16'),
            ('int32_t', 'int32'),
            ('uint32_t', 'uint32'),
            ('int64_t', 'int64'),
            ('uint64_t', 'uint64'),
            ('int', 'int'),
            ('unsigned_int', 'uint'),
            ('float', 'float'),
            ('double', 'double'),
        ] %}
        {
            auto c_type = PyObject_GetAttrString(ctypes, "c_{{ ctypes_name }}");
            if (!c_type)
            {
                Py_DECREF(ctypes_pointer);
                Py_DECREF(ctypes);
                goto error;
            }
            state->ctypes_c_{{ c_type }}_p = PyObject_CallFunction(ctypes_pointer, "O", c_type);
            if (!state->ctypes_c_{{ c_type }}_p)
            {
                Py_DECREF(ctypes_pointer);
                Py_DECREF(ctypes);
                goto error;
            }
        }
        {% endfor %}

        Py_DECREF(ctypes_pointer);
        Py_DECREF(ctypes);
    }

    {% for type in vector_types %}
        {
            PyTypeObject *type = define_{{ type }}_type(module);
            if (!type){ goto error; }
            Py_INCREF(type);
            state->{{ type }}_PyTypeObject = type;
        }
        {
            PyTypeObject *type = define_{{ type }}Array_type(module);
            if (!type){ goto error; }
            Py_INCREF(type);
            state->{{ type }}Array_PyTypeObject = type;
        }
        api->{{ type }}_GetType = get_{{ type }}_type;
        api->{{ type }}Array_GetType = get_{{ type }}Array_type;
        api->{{ type }}_Create = create_{{ type }};
        api->{{ type }}Array_Create = create_{{ type }}Array;
        api->{{ type }}_GetValuePointer = get_{{ type }}_value_ptr;
        api->{{ type }}Array_GetValuePointer = get_{{ type }}Array_value_ptr;
        api->{{ type }}Array_GetLength = get_{{ type }}Array_length;
    {% endfor %}
    {% for type in matrix_types %}
        {
            PyTypeObject *type = define_{{ type }}_type(module);
            if (!type){ goto error; }
            Py_INCREF(type);
            state->{{ type }}_PyTypeObject = type;
        }
        {
            PyTypeObject *type = define_{{ type }}Array_type(module);
            if (!type){ goto error; }
            Py_INCREF(type);
            state->{{ type }}Array_PyTypeObject = type;
        }
        api->{{ type }}_GetType = get_{{ type }}_type;
        api->{{ type }}Array_GetType = get_{{ type }}Array_type;
        api->{{ type }}_Create = create_{{ type }};
        api->{{ type }}Array_Create = create_{{ type }}Array;
        api->{{ type }}_GetValuePointer = get_{{ type }}_value_ptr;
        api->{{ type }}Array_GetValuePointer = get_{{ type }}Array_value_ptr;
        api->{{ type }}Array_GetLength = get_{{ type }}Array_length;
    {% endfor %}
    {% for type in quaternion_types %}
        {
            PyTypeObject *type = define_{{ type }}_type(module);
            if (!type){ goto error; }
            Py_INCREF(type);
            state->{{ type }}_PyTypeObject = type;
        }
        {
            PyTypeObject *type = define_{{ type }}Array_type(module);
            if (!type){ goto error; }
            Py_INCREF(type);
            state->{{ type }}Array_PyTypeObject = type;
        }
        api->{{ type }}_GetType = get_{{ type }}_type;
        api->{{ type }}Array_GetType = get_{{ type }}Array_type;
        api->{{ type }}_Create = create_{{ type }};
        api->{{ type }}Array_Create = create_{{ type }}Array;
        api->{{ type }}_GetValuePointer = get_{{ type }}_value_ptr;
        api->{{ type }}Array_GetValuePointer = get_{{ type }}Array_value_ptr;
        api->{{ type }}Array_GetLength = get_{{ type }}Array_length;
    {% endfor %}
    {% for type in pod_types %}
        {
            PyTypeObject *type = define_{{ type }}Array_type(module);
            if (!type){ goto error; }
            Py_INCREF(type);
            state->{{ type }}Array_PyTypeObject = type;
        }
        api->{{ type }}Array_GetType = get_{{ type }}Array_type;
        api->{{ type }}Array_Create = create_{{ type }}Array;
        api->{{ type }}Array_GetValuePointer = get_{{ type }}Array_value_ptr;
        api->{{ type }}Array_GetLength = get_{{ type }}Array_length;
    {% endfor %}

    if (PyModule_AddObject(module, "_api", api_capsule) < 0){ goto error; }

    return module;
error:
    delete api;
    Py_DECREF(api_capsule);
    Py_CLEAR(module);
    return 0;
}


static PyObject *
get_module()
{
    PyObject *module = PyState_FindModule(&module_PyModuleDef);
    if (!module)
    {
        return PyErr_Format(PyExc_RuntimeError, "math module not ready");
    }
    return module;
}
